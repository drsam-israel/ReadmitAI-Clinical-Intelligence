# ============================================================
# READMITAI CLINICAL INTELLIGENCE
# 30-Day Readmission Clinical Decision-Support Prototype
# ============================================================


# ============================================================
# DEPLOYMENT PATH BOOTSTRAP
# ============================================================
# Ensures the repository root is available when Streamlit
# Community Cloud executes app/readmitai.py directly.
# ============================================================

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# APPLICATION DEPENDENCIES
# ============================================================

import streamlit as st
import pandas as pd
import altair as alt


# ============================================================
# READMITAI APPLICATION SERVICES
# ============================================================

from app.services.inference_service import run_readmission_inference
from app.services.explainability_service import explain_readmission_prediction
from app.services.explainability_evidence_service import (
    get_global_explainability_context,
)
from app.services.model_evidence_service import get_model_evidence
from app.services.monitoring_evidence_service import get_monitoring_evidence
# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ReadmitAI Clinical Intelligence",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# APPLICATION CONSTANTS
# ============================================================

MODEL_NAME = "DIABETES_READMISSION_XGB_D13_V1"
MODEL_VERSION = "1.0.0"
OPERATING_THRESHOLD = 0.12

APPLICATION_STATUS = "Research & Validation"
DEPLOYMENT_STATUS = "Production Not Authorized"


# ============================================================
# ENTERPRISE UI STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */
    .stApp {
        background-color: #F7F9FC;
    }

    /* Main content */
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #142238;
    }

    [data-testid="stSidebar"] * {
        color: #F4F7FB;
    }

    /* Operational header */
    .readmit-header {
        background: #FFFFFF;
        border: 1px solid #E1E7EF;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 18px;
    }

    .readmit-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #17263C;
        margin: 0;
    }

    .readmit-subtitle {
        font-size: 0.88rem;
        color: #66758A;
        margin-top: 3px;
    }

    /* Status badges */
    .status-row {
        margin-top: 10px;
    }

    .status-badge {
        display: inline-block;
        padding: 4px 9px;
        margin-right: 6px;
        margin-bottom: 4px;
        border-radius: 5px;
        font-size: 0.72rem;
        font-weight: 600;
        border: 1px solid #D7DFE9;
        background: #F5F7FA;
        color: #33445A;
    }

    .status-warning {
        background: #FFF6E6;
        border-color: #E8C77B;
        color: #72520A;
    }

    /* Workspace cards */
    .workspace-card {
        background: #FFFFFF;
        border: 1px solid #E1E7EF;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .workspace-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1B2A41;
        margin-bottom: 5px;
    }

    .workspace-text {
        color: #617086;
        font-size: 0.9rem;
        line-height: 1.55;
    }

    /* Footer */
    .readmit-footer {
        margin-top: 40px;
        padding-top: 15px;
        border-top: 1px solid #DCE3EC;
        color: #718096;
        font-size: 0.75rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR — APPLICATION NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown("## ReadmitAI")
    st.caption("Clinical Intelligence")

    st.markdown("---")

    page = st.radio(
        "Clinical Workspace",
        [
            "Risk Assessment",
            "Explainability",
            "Model Evidence",
            "Governance & Safety",
            "Monitoring",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.caption("MODEL")
    st.write(f"Version {MODEL_VERSION}")

    st.caption("STATUS")
    st.write(APPLICATION_STATUS)

    st.caption("DEPLOYMENT")
    st.write(DEPLOYMENT_STATUS)


# ============================================================
# PERSISTENT OPERATIONAL HEADER
# ============================================================

st.markdown(
    f"""
<div class="readmit-header">
    <div class="readmit-title">ReadmitAI | 30-Day Readmission Clinical Decision-Support</div>
    <div class="readmit-subtitle">Clinical Risk Intelligence · Explainability · Governance · Monitoring</div>
    <div class="status-row">
        <span class="status-badge">Research & Validation</span>
        <span class="status-badge">Model v{MODEL_VERSION}</span>
        <span class="status-badge status-warning">Production Not Authorized</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PAGE — RISK ASSESSMENT
# ============================================================

if page == "Risk Assessment":

    st.subheader("Risk Assessment")

    st.caption(
        "Enter the information available at the assessment point. "
        "Inputs are translated into the frozen model feature contract."
    )

    # --------------------------------------------------------
    # GOVERNED DISPLAY MAPPINGS
    # --------------------------------------------------------

    race_options = [
        "AfricanAmerican",
        "Asian",
        "Caucasian",
        "Hispanic",
        "Other",
        "__MISSING_OR_UNKNOWN__",
    ]

    gender_options = [
        "Female",
        "Male",
        "__MISSING_OR_UNKNOWN__",
    ]

    age_options = [
        "[0-10)",
        "[10-20)",
        "[20-30)",
        "[30-40)",
        "[40-50)",
        "[50-60)",
        "[60-70)",
        "[70-80)",
        "[80-90)",
        "[90-100)",
    ]

    admission_type_options = {
        "Emergency": 1,
        "Urgent": 2,
        "Elective": 3,
        "Newborn": 4,
        "Not Available": 5,
        "NULL": 6,
        "Trauma Center": 7,
        "Not Mapped": 8,
    }

    admission_source_options = {
        "Physician Referral": 1,
        "Clinic Referral": 2,
        "HMO Referral": 3,
        "Transfer from a hospital": 4,
        "Transfer from a Skilled Nursing Facility (SNF)": 5,
        "Transfer from another health care facility": 6,
        "Emergency Room": 7,
        "Court/Law Enforcement": 8,
        "Not Available": 9,
        "Transfer from critical access hospital": 10,
        "Normal Delivery": 11,
        "Sick Baby": 13,
        "Extramural Birth": 14,
        "NULL": 17,
        "Not Mapped": 20,
        "Transfer from hospital inpatient / same facility separate claim": 22,
        "Transfer from Ambulatory Surgery Center": 25,
    }

    # --------------------------------------------------------
    # CLINICAL INPUT FORM
    # --------------------------------------------------------

    with st.form("readmission_assessment_form"):

        col1, col2, col3 = st.columns(3)

        # ----------------------------------------------------
        # PATIENT PROFILE
        # ----------------------------------------------------

        with col1:

            st.markdown("### Patient Profile")

            race = st.selectbox(
                "Race",
                options=race_options,
                index=None,
                placeholder="Select race",
            )

            gender = st.selectbox(
                "Gender",
                options=gender_options,
                index=None,
                placeholder="Select gender",
            )

            age = st.selectbox(
                "Age",
                options=age_options,
                index=None,
                placeholder="Select age band",
            )

        # ----------------------------------------------------
        # ADMISSION CONTEXT
        # ----------------------------------------------------

        with col2:

            st.markdown("### Admission Context")

            admission_type_label = st.selectbox(
                "Admission Type",
                options=list(admission_type_options.keys()),
                index=None,
                placeholder="Select admission type",
            )

            admission_source_label = st.selectbox(
                "Admission Source",
                options=list(admission_source_options.keys()),
                index=None,
                placeholder="Select admission source",
            )

        # ----------------------------------------------------
        # PRIOR HEALTHCARE UTILIZATION
        # ----------------------------------------------------

        with col3:

            st.markdown("### Prior Healthcare Utilization")

            number_outpatient = st.number_input(
                "Prior Outpatient Visits",
                min_value=0,
                step=1,
                value=0,
                help=(
                    "Number of outpatient encounters recorded "
                    "before the current encounter."
                ),
            )

            number_emergency = st.number_input(
                "Prior Emergency Visits",
                min_value=0,
                step=1,
                value=0,
                help=(
                    "Number of emergency encounters recorded "
                    "before the current encounter."
                ),
            )

            number_inpatient = st.number_input(
                "Prior Inpatient Admissions",
                min_value=0,
                step=1,
                value=0,
                help=(
                    "Number of inpatient admissions recorded "
                    "before the current encounter."
                ),
            )

        st.markdown("---")

        submitted = st.form_submit_button(
            "Run Readmission Assessment",
            type="primary",
            use_container_width=True,
        )
    # --------------------------------------------------------
    # GOVERNED INFERENCE
    # --------------------------------------------------------

    if "assessment_result" not in st.session_state:
        st.session_state.assessment_result = None

    if submitted:

        required_fields_complete = all(
            [
                race is not None,
                gender is not None,
                age is not None,
                admission_type_label is not None,
                admission_source_label is not None,
            ]
        )

        if not required_fields_complete:

            st.session_state.assessment_result = None

            st.error(
                "Assessment not run. Complete all required "
                "patient and admission fields."
            )

        else:

            admission_type_id = (
                admission_type_options[admission_type_label]
            )

            admission_source_id = (
                admission_source_options[admission_source_label]
            )

            try:

                result = run_readmission_inference(
                    race=race,
                    gender=gender,
                    age=age,
                    admission_type_id=admission_type_id,
                    admission_source_id=admission_source_id,
                    number_outpatient=int(number_outpatient),
                    number_emergency=int(number_emergency),
                    number_inpatient=int(number_inpatient),
                )

                st.session_state.assessment_result = result
                st.session_state.assessment_inputs = {
                   "race": race,
                   "gender": gender,
                   "age": age,
                   "admission_type_id": admission_type_id,
                   "admission_source_id": admission_source_id,
                   "number_outpatient": int(number_outpatient),
                   "number_emergency": int(number_emergency),
                   "number_inpatient": int(number_inpatient),
                }

            except Exception as exc:

                st.session_state.assessment_result = None

                st.error(
                    "Assessment could not be completed because "
                    "the governed inference pipeline returned an error."
                )

                st.exception(exc)

    # --------------------------------------------------------
    # ASSESSMENT OUTPUT
    # --------------------------------------------------------

    st.markdown("### Assessment Output")

    result = st.session_state.assessment_result

    output1, output2, output3 = st.columns(3)

    if result is None:

        output1.metric(
            "30-Day Readmission Probability",
            "—",
        )

        output2.metric(
            "Operating Threshold",
            f"{OPERATING_THRESHOLD:.0%}",
        )

        output3.metric(
            "Model Advisory",
            "—",
        )

        st.info(
            "No assessment has been performed. "
            "Complete the clinical inputs and run the assessment."
        )

    else:

        probability = result["probability"]

        output1.metric(
            "30-Day Readmission Probability",
            f"{probability:.1%}",
        )

        output2.metric(
            "Operating Threshold",
            f"{result['operating_threshold']:.0%}",
        )

        output3.metric(
            "Model Advisory",
            result["advisory"],
        )

        # ----------------------------------------------------
        # CLINICAL INTERPRETATION
        # ----------------------------------------------------

        if result["priority_flag"]:

            st.warning(
                "The model-estimated probability exceeds the "
                "frozen development-stage operating threshold. "
                "The model therefore recommends prioritization "
                "for additional human readmission-prevention review."
            )

        else:

            st.info(
                "The model-estimated probability is below the "
                "frozen development-stage operating threshold. "
                "No model priority flag was generated."
            )

        st.caption(
            "This is a prioritization signal. It does not establish "
            "that the patient will or will not be readmitted."
        )

        # ----------------------------------------------------
        # ZERO-UTILIZATION SAFETY CONTROL
        # ----------------------------------------------------

        if result["zero_prior_utilization"]:

            st.error(
                "MODEL LIMITATION — PRIOR UTILIZATION\n\n"
                "This patient has no recorded prior outpatient, "
                "emergency, or inpatient utilization. In internal "
                "locked-test evaluation, the model demonstrated "
                "0% sensitivity within this utilization profile at "
                "the frozen operating threshold. Absence of a model "
                "priority flag must not be interpreted as absence "
                "of readmission risk."
            )

        # ----------------------------------------------------
        # GOVERNED UTILIZATION SUMMARY
        # ----------------------------------------------------

        utilization = result["utilization_summary"]

        with st.expander(
            "Governed utilization transformation",
            expanded=False,
        ):

            u1, u2, u3, u4, u5 = st.columns(5)

            u1.metric(
                "Outpatient Use",
                utilization["prior_outpatient_use"],
            )

            u2.metric(
                "Emergency Use",
                utilization["prior_emergency_use"],
            )

            u3.metric(
                "Inpatient Use",
                utilization["prior_inpatient_use"],
            )

            u4.metric(
                "Utilization Intensity",
                utilization["prior_utilization_intensity"],
            )

            u5.metric(
                "Utilization Domains",
                utilization["prior_utilization_domain_count"],
            )

        # ----------------------------------------------------
        # HUMAN CLINICAL DECISION AUTHORITY
        # ----------------------------------------------------

        st.markdown(
            """
            **Clinical decision authority**

            This model does not determine discharge, diagnosis,
            treatment, eligibility for care, or other autonomous
            clinical decisions. Clinical judgment remains
            authoritative.
            """
        )
# ============================================================
# PAGE — EXPLAINABILITY
# ============================================================

elif page == "Explainability":

    st.subheader("Explainability")

    st.caption(
        "Patient-level model contribution analysis and global "
        "model-behavior context."
    )

    # --------------------------------------------------------
    # RETRIEVE CURRENT PATIENT ASSESSMENT
    # --------------------------------------------------------

    assessment_result = st.session_state.get(
        "assessment_result"
    )

    assessment_inputs = st.session_state.get(
        "assessment_inputs"
    )

    # --------------------------------------------------------
    # REQUIRE A COMPLETED ASSESSMENT
    # --------------------------------------------------------

    if (
        assessment_result is None
        or assessment_inputs is None
    ):
        st.info(
            "No patient assessment is currently available. "
            "Complete a Risk Assessment first to generate "
            "a patient-level model explanation."
        )

        st.markdown(
            """
            **Interpretation principle**

            Patient-level explanations are generated only for an
            assessment actually processed by the frozen ReadmitAI
            model. Model contributions describe model behavior and
            must not be interpreted as clinical causality.
            """
        )

        st.stop()

    # --------------------------------------------------------
    # GENERATE GOVERNED PATIENT-LEVEL EXPLANATION
    # --------------------------------------------------------

    try:
        patient_explanation = explain_readmission_prediction(
            **assessment_inputs
        )

    except Exception as exc:
        st.error(
            "Patient-level model explanation could not be generated. "
            "The prediction remains available, but the explanation "
            "should not be interpreted until this issue is resolved."
        )

        st.exception(exc)
        st.stop()

    # --------------------------------------------------------
    # PRESERVE EXPLANATION IN SESSION STATE
    # --------------------------------------------------------

    st.session_state.patient_explanation = patient_explanation

        # --------------------------------------------------------
    # LOAD VALIDATED D12 GLOBAL EXPLAINABILITY EVIDENCE
    # --------------------------------------------------------

    try:
        global_context = get_global_explainability_context()

    except Exception as exc:
        st.error(
            "Validated global explainability evidence could not "
            "be loaded from the D12 evidence record."
        )
        st.exception(exc)
        st.stop()

    # --------------------------------------------------------
    # PREDICTION TRACEABILITY
    # --------------------------------------------------------

    prediction_probability = assessment_result[
        "probability"
    ]

    explanation_probability = patient_explanation[
        "probability"
    ]

    reconstructed_probability = patient_explanation[
        "reconstructed_probability"
    ]

    reconstruction_error = patient_explanation[
        "probability_reconstruction_error"
    ]

    st.markdown("### Current Assessment")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "30-Day Readmission Probability",
        f"{prediction_probability:.1%}",
    )

    col2.metric(
        "Operating Threshold",
        f"{assessment_result['operating_threshold']:.0%}",
    )

    col3.metric(
        "Model Advisory",
        assessment_result["advisory"],
    )

    # --------------------------------------------------------
    # EXPLANATION TRACEABILITY CONTROL
    # --------------------------------------------------------

    if abs(
        prediction_probability
        - explanation_probability
    ) > 1e-6:
        st.error(
            "EXPLANATION TRACEABILITY FAILURE — "
            "The probability associated with this explanation "
            "does not match the current patient assessment."
        )
        st.stop()

    st.success(
        "Prediction-to-explanation traceability verified. "
        "The explanation corresponds to the current patient assessment."
    )

    # --------------------------------------------------------
    # MODEL CONTRIBUTION INTERPRETATION
    # --------------------------------------------------------

    st.markdown("### Patient-Level Model Contributions")

    st.caption(
        "Model contribution — not clinical causality. "
        "SHAP values describe contribution to the model's raw "
        "output (margin/log-odds), not direct percentage-point "
        "changes in readmission probability."
    )

    contributions = patient_explanation[
        "source_family_contributions"
    ]

    # --------------------------------------------------------
    # CLINICIAN-FRIENDLY FEATURE LABELS
    # --------------------------------------------------------

    feature_labels = {
        "race": "Race",
        "gender": "Gender",
        "age": "Age",
        "admission_type_id": "Admission Type",
        "admission_source_id": "Admission Source",
        "prior_outpatient_use": "Prior Outpatient Use",
        "prior_emergency_use": "Prior Emergency Use",
        "prior_inpatient_use": "Prior Inpatient Use",
        "prior_utilization_intensity": "Prior Utilization Intensity",
        "prior_utilization_domain_count": "Prior Utilization Domains",
    }

    # --------------------------------------------------------
    # DISPLAY RANKED CONTRIBUTIONS
    # --------------------------------------------------------

        # --------------------------------------------------------
    # ENTERPRISE PATIENT-LEVEL CONTRIBUTION VISUALIZATION
    # --------------------------------------------------------

    contribution_rows = []

    for contribution in contributions:

        source_feature = contribution[
            "source_feature_family"
        ]

        shap_value = float(
            contribution["shap_value"]
        )

        contribution_rows.append(
            {
                "Feature": feature_labels.get(
                    source_feature,
                    source_feature,
                ),
                "SHAP Contribution": shap_value,
                "Direction": (
                    "Toward higher model output"
                    if shap_value > 0
                    else
                    "Toward lower model output"
                    if shap_value < 0
                    else
                    "Neutral"
                ),
                "Magnitude": abs(shap_value),
            }
        )

    contribution_df = pd.DataFrame(
        contribution_rows
    )

    # Largest model contributions appear first.
    contribution_df = contribution_df.sort_values(
        "Magnitude",
        ascending=False,
    )

    feature_order = contribution_df[
        "Feature"
    ].tolist()

    contribution_chart = (
        alt.Chart(contribution_df)
        .mark_bar(
            cornerRadiusEnd=3,
            size=18,
        )
        .encode(
            x=alt.X(
                "SHAP Contribution:Q",
                title="Contribution to raw model output (SHAP value)",
                axis=alt.Axis(
                    format=".2f",
                    grid=True,
                ),
            ),
            y=alt.Y(
                "Feature:N",
                title=None,
                sort=feature_order,
                axis=alt.Axis(
                    labelLimit=240,
                ),
            ),
            color=alt.Color(
                "Direction:N",
                title=None,
                scale=alt.Scale(
                    domain=[
                        "Toward higher model output",
                        "Toward lower model output",
                        "Neutral",
                    ],
                    range=[
                        "#2F6B5F",
                        "#9A5B5B",
                        "#7A8798",
                    ],
                ),
                legend=alt.Legend(
                    orient="top",
                    direction="horizontal",
                ),
            ),
            tooltip=[
                alt.Tooltip(
                    "Feature:N",
                    title="Feature",
                ),
                alt.Tooltip(
                    "Direction:N",
                    title="Direction",
                ),
                alt.Tooltip(
                    "SHAP Contribution:Q",
                    title="Raw SHAP contribution",
                    format="+.4f",
                ),
            ],
        )
        .properties(
            height=360,
        )
    )

    zero_reference = (
        alt.Chart(
            pd.DataFrame(
                {"zero": [0.0]}
            )
        )
        .mark_rule(
            strokeWidth=1.5,
            color="#526274",
        )
        .encode(
            x="zero:Q"
        )
    )

    final_contribution_chart = (
        contribution_chart
        + zero_reference
    )

    st.altair_chart(
        final_contribution_chart,
        use_container_width=True,
    )

    st.caption(
        "Bars to the right of zero contributed toward a higher "
        "raw model output; bars to the left contributed toward a "
        "lower raw model output. Magnitude represents model "
        "attribution strength for this assessment."
    )

    st.info(
        "SHAP contributions are expressed in the frozen model's "
        "raw margin/log-odds space. They are not direct changes "
        "in readmission probability and do not represent causal "
        "clinical effects."
    )

        # --------------------------------------------------------
    # GLOBAL MODEL CONTEXT — VALIDATED D12 EVIDENCE
    # --------------------------------------------------------

    st.markdown("### Global Model Context")

    utilization_attribution = global_context[
        "prior_utilization_absolute_attribution_percent"
    ]

    global1, global2, global3 = st.columns(3)

    global1.metric(
        "Prior-Utilization Attribution",
        f"{utilization_attribution:.1f}%",
    )

    global2.metric(
        "Source-Feature Families",
        global_context["source_feature_family_count"],
    )

    global3.metric(
        "Attribution Stability Slices",
        global_context["attribution_stability_slice_count"],
    )

    st.markdown(
        f"""
        Across the D12 validation explainability analysis,
        **{utilization_attribution:.2f}% of total mean absolute model
        attribution** was associated with the five governed
        prior-utilization feature families:

        - Prior Outpatient Use
        - Prior Emergency Use
        - Prior Inpatient Use
        - Prior Utilization Intensity
        - Prior Utilization Domain Count

        This indicates substantial model dependence on recorded prior
        healthcare-utilization information. It does **not** establish
        that prior utilization causes 30-day readmission.
        """
    )

    st.warning(
        "GLOBAL EXPLAINABILITY LIMITATION — The model demonstrates "
        "substantial dependence on prior healthcare-utilization "
        "features. Patient-level explanations should therefore be "
        "interpreted alongside utilization availability and the "
        "model's known utilization-dependent behavior."
    )

    with st.expander(
        "D12 global explainability evidence",
        expanded=False,
    ):
        evidence1, evidence2, evidence3 = st.columns(3)

        evidence1.metric(
            "Validation Encounters",
            f"{global_context['validation_encounters']:,}",
        )

        evidence2.metric(
            "Adequate-Support Slices",
            global_context["adequate_support_slice_count"],
        )

        evidence3.metric(
            "Low-Support Slices",
            global_context["low_support_slice_count"],
        )

        st.write(
            "Causality established:",
            global_context["causality_established"],
        )

        st.write(
            "External validation established:",
            global_context["external_validation_established"],
        )

        st.caption(
            "Global attribution evidence is loaded from the persisted "
            "D12 explainability validation record. Global SHAP is not "
            "recomputed by the application at runtime."
        )

    # --------------------------------------------------------
    # MATHEMATICAL TRACEABILITY
    # --------------------------------------------------------

    with st.expander(
        "Explanation traceability",
        expanded=False,
    ):

        trace1, trace2, trace3 = st.columns(3)

        trace1.metric(
            "Model Probability",
            f"{explanation_probability:.6f}",
        )

        trace2.metric(
            "SHAP-Reconstructed Probability",
            f"{reconstructed_probability:.6f}",
        )

        trace3.metric(
            "Reconstruction Error",
            f"{reconstruction_error:.2e}",
        )

        st.caption(
            "The frozen model prediction is reconstructed from the "
            "SHAP base value plus patient-level SHAP contributions "
            "in raw model-output space, followed by the logistic "
            "probability transformation."
        )

    # --------------------------------------------------------
    # GOVERNANCE INTERPRETATION
    # --------------------------------------------------------

    st.markdown("### Interpretation & Safety")

    st.warning(
        "SHAP attribution describes how the frozen model generated "
        "this prediction. It does not establish biological mechanism, "
        "clinical causality, treatment effect, or future certainty."
    )

    st.markdown(
        """
        **Clinical interpretation**

        The contribution pattern should be interpreted alongside the
        model's known dependence on prior healthcare-utilization
        information and the broader validation evidence.

        A feature contributing toward a higher model output does not
        mean that the feature causes readmission. Likewise, a feature
        contributing toward a lower model output does not establish
        protection from readmission.

        **Human decision authority**

        This explanation supports interpretation of the model signal.
        It does not replace clinician assessment and must not be used
        independently to determine discharge, diagnosis, treatment,
        eligibility for care, or other clinical decisions.
        """
    )

# ============================================================
# PAGE — MODEL EVIDENCE
# ============================================================

elif page == "Model Evidence":

    st.subheader("Model Evidence")

    st.caption(
        "Locked-test validation evidence, frozen operating characteristics, "
        "generalization stability and governance disposition."
    )

    # ========================================================
    # MODEL EVIDENCE — COMPACT ENTERPRISE UI
    # ========================================================

    st.markdown(
        """
        <style>

        /* Model Evidence metric cards */
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 14px 16px 12px 16px;
            min-height: 108px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        /* Metric label */
        div[data-testid="stMetricLabel"] {
            font-size: 0.82rem;
            font-weight: 600;
            color: #475569;
            line-height: 1.25;
        }

        /* Metric value — deliberately smaller */
        div[data-testid="stMetricValue"] {
            font-size: 1.65rem;
            font-weight: 600;
            color: #172B4D;
            line-height: 1.15;
        }

        /* Reduce vertical whitespace between metric rows */
        div[data-testid="stHorizontalBlock"] {
            gap: 0.85rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    # ========================================================
    # LOAD AUTHORITATIVE D14 EVIDENCE
    # ========================================================

    try:
        evidence = get_model_evidence()
    except Exception as exc:
        st.error(
            "Model Evidence could not be loaded from the authoritative "
            "D14 evidence artifacts."
        )
        st.exception(exc)
        st.stop()

    # ========================================================
    # VALIDATION STATUS
    # ========================================================

    st.markdown("### Validation Status")

    status_col1, status_col2, status_col3, status_col4 = st.columns(4)

    with status_col1:
        st.metric(
            "Internal Locked-Test Validation",
            "COMPLETED",
        )

    with status_col2:
        st.metric(
            "External Validation",
            evidence["external_validation_status"].replace("_", " "),
        )

    with status_col3:
        st.metric(
            "Clinical Effectiveness",
            evidence["clinical_effectiveness_status"].replace("_", " "),
        )

    with status_col4:
        st.metric(
            "Production Deployment",
            evidence["deployment_status"].replace("_", " "),
        )

    st.warning(
        "Internal locked-test validation has been completed. "
        "External validation and clinical effectiveness have not been "
        "established, and production deployment is not authorized."
    )

    # ========================================================
    # FROZEN EVALUATION CONTRACT
    # ========================================================

    st.markdown("### Frozen Evaluation Contract")

    contract_col1, contract_col2, contract_col3, contract_col4 = st.columns(4)

    with contract_col1:
        st.metric(
            "Operating Threshold",
            f"{evidence['frozen_threshold']:.0%}",
        )

    with contract_col2:
        st.metric(
            "Evaluation Partition",
            evidence["evaluation_partition"].replace("_", " ").title(),
        )

    with contract_col3:
        st.metric(
            "Evaluation Mode",
            evidence["evaluation_mode"].replace("_", " ").title(),
        )

    with contract_col4:
        st.metric(
            "Gate Integrity",
            evidence["gate_integrity_status"],
        )

    st.caption(
        f"Frozen candidate: {evidence['registry_id']} · "
        "Performance is loaded from persisted D14 evidence and is not "
        "recomputed at application runtime."
    )

    # ========================================================
    # LOCKED-TEST COHORT
    # ========================================================

    st.markdown("### Locked-Test Cohort")

    cohort_col1, cohort_col2, cohort_col3, cohort_col4 = st.columns(4)

    with cohort_col1:
        st.metric(
            "Encounters",
            f"{evidence['encounter_count']:,}",
        )

    with cohort_col2:
        st.metric(
            "30-Day Readmissions",
            f"{evidence['positive_count']:,}",
        )

    with cohort_col3:
        st.metric(
            "Non-Readmissions",
            f"{evidence['negative_count']:,}",
        )

    with cohort_col4:
        st.metric(
            "Readmission Prevalence",
            f"{evidence['prevalence']:.2%}",
        )

    # ========================================================
    # LOCKED-TEST PERFORMANCE
    # ========================================================

    st.markdown("### Locked-Test Performance")

    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)

    with perf_col1:
        st.metric(
            "ROC-AUC",
            f"{evidence['roc_auc']:.3f}",
        )

    with perf_col2:
        st.metric(
            "PR-AUC",
            f"{evidence['pr_auc']:.3f}",
        )

    with perf_col3:
        st.metric(
            "Sensitivity",
            f"{evidence['sensitivity']:.2%}",
        )

    with perf_col4:
        st.metric(
            "Specificity",
            f"{evidence['specificity']:.2%}",
        )

    perf_col5, perf_col6, perf_col7, perf_col8 = st.columns(4)

    with perf_col5:
        st.metric(
            "Positive Predictive Value",
            f"{evidence['precision_ppv']:.2%}",
        )

    with perf_col6:
        st.metric(
            "Negative Predictive Value",
            f"{evidence['negative_predictive_value']:.2%}",
        )

    with perf_col7:
        st.metric(
            "F1 Score",
            f"{evidence['f1_score']:.3f}",
        )

    with perf_col8:
        st.metric(
            "Alert Rate",
            f"{evidence['alert_rate']:.2%}",
        )

    st.info(
        "Locked-test discrimination remained modest. These predictive "
        "performance measures do not establish clinical effectiveness, "
        "external transportability, or suitability for autonomous "
        "clinical decision-making."
    )

    # ========================================================
    # OPERATING CONSEQUENCES
    # ========================================================

    st.markdown("### Operating Consequences at the Frozen Threshold")

    op_col1, op_col2, op_col3 = st.columns(3)

    with op_col1:
        st.metric(
            "Alerts",
            f"{evidence['alert_count']:,}",
        )

    with op_col2:
        st.metric(
            "Alerts / 100 Encounters",
            f"{evidence['alerts_per_100_encounters']:.2f}",
        )

    with op_col3:
        st.metric(
            "Number Needed to Evaluate",
            f"{evidence['number_needed_to_evaluate']:.2f}",
        )

    confusion_df = pd.DataFrame(
        {
            "Observed Outcome": [
                "30-Day Readmission",
                "No 30-Day Readmission",
            ],
            "Model Priority Flag": [
                evidence["true_positives"],
                evidence["false_positives"],
            ],
            "No Model Priority Flag": [
                evidence["false_negatives"],
                evidence["true_negatives"],
            ],
        }
    )

    st.dataframe(
        confusion_df,
        hide_index=True,
        width="stretch",
    )

    st.caption(
        "Operating consequences reflect the frozen 0.12 threshold. "
        "A model priority flag is a review signal and is not a clinical "
        "diagnosis or determination that readmission will occur."
    )

    # ========================================================
    # VALIDATION → LOCKED-TEST STABILITY
    # ========================================================

    st.markdown("### Validation → Locked-Test Stability")

    comparison_df = pd.DataFrame(
        evidence["validation_test_comparison"]
    )

    display_metrics = [
        "prevalence",
        "pr_auc",
        "roc_auc",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "alert_rate",
    ]

    stability_df = comparison_df[
        comparison_df["metric"].isin(display_metrics)
    ].copy()

    metric_labels = {
        "prevalence": "Prevalence",
        "pr_auc": "PR-AUC",
        "roc_auc": "ROC-AUC",
        "sensitivity": "Sensitivity",
        "specificity": "Specificity",
        "precision_ppv": "PPV",
        "negative_predictive_value": "NPV",
        "alert_rate": "Alert Rate",
    }

    stability_df["Metric"] = stability_df["metric"].map(metric_labels)

    percentage_metrics = {
        "prevalence",
        "sensitivity",
        "specificity",
        "precision_ppv",
        "negative_predictive_value",
        "alert_rate",
    }

    def format_stability_value(metric, value):
        if metric in percentage_metrics:
            return f"{float(value):.2%}"
        return f"{float(value):.4f}"

    stability_df["Validation"] = stability_df.apply(
        lambda row: format_stability_value(
            row["metric"],
            row["validation"],
        ),
        axis=1,
    )

    stability_df["Locked Test"] = stability_df.apply(
        lambda row: format_stability_value(
            row["metric"],
            row["locked_test"],
        ),
        axis=1,
    )

    stability_df["Test − Validation"] = stability_df.apply(
        lambda row: (
            f"{float(row['absolute_difference_test_minus_validation']) * 100:+.2f} pp"
            if row["metric"] in percentage_metrics
            else f"{float(row['absolute_difference_test_minus_validation']):+.4f}"
        ),
        axis=1,
    )

    st.dataframe(
        stability_df[
            [
                "Metric",
                "Validation",
                "Locked Test",
                "Test − Validation",
            ]
        ],
        hide_index=True,
        width="stretch",
    )

    st.caption(
        "The locked-test evaluation was confirmatory. "
        "Observed validation-to-test differences are presented descriptively "
        "and were not used to retrain the model or retune the operating threshold."
    )

    # ========================================================
    # RESIDUAL RISK REGISTER
    # ========================================================

    st.markdown("### Residual Risk & Model Limitations")

    st.warning(
        f"{evidence['unresolved_residual_risk_count']} unresolved residual "
        "risks were carried forward from D14. Internal validation completion "
        "does not mean these risks have been resolved."
    )

    for risk in evidence["residual_risks"]:

        risk_domain = str(
            risk.get("risk_domain", "UNSPECIFIED")
        ).replace("_", " ").title()

        risk_id = str(
            risk.get("risk_id", "UNSPECIFIED")
        )

        severity = str(
            risk.get("severity_classification", "UNSPECIFIED")
        )

        with st.expander(
            f"{risk_id} · {risk_domain} · {severity}"
        ):
            st.markdown(
                f"**Finding:** {risk.get('finding', 'Not documented.')}"
            )

            st.markdown(
                f"**Evidence:** {risk.get('evidence', 'Not documented.')}"
            )

            st.markdown(
                f"**Interpretation:** "
                f"{risk.get('interpretation', 'Not documented.')}"
            )

            st.markdown(
                f"**Required Control:** "
                f"{risk.get('required_control', 'Not documented.')}"
            )

            st.caption(
                "Resolution status: "
                + (
                    "Resolved"
                    if bool(risk.get("resolved", False))
                    else "Unresolved"
                )
            )

    # ========================================================
    # GOVERNANCE DISPOSITION
    # ========================================================

    st.markdown("### Governance Disposition")

    st.success(
        "D14 locked-test evaluation completed with gate integrity preserved."
    )

    st.markdown(
        f"**Disposition:** "
        f"{evidence['disposition'].replace('_', ' ')}"
    )

    st.markdown(
        "**Clinical interpretation:** The frozen candidate demonstrated "
        "internal locked-test predictive performance sufficient to complete "
        "the D14 evaluation gate, while material and unresolved limitations "
        "remain. The evidence does not establish external transportability "
        "or clinical effectiveness and does not authorize production deployment."
    )

    with st.expander("Evidence provenance"):
        st.write(
            "Performance evidence:",
            evidence["performance_evidence_source"],
        )
        st.write(
            "Validation/test comparison:",
            evidence["comparison_evidence_source"],
        )
        st.write(
            "Governance evidence:",
            evidence["governance_evidence_source"],
        )
        st.write(
            "Runtime performance recomputation:",
            evidence["runtime_performance_recomputed"],
        )
        st.write(
            "Model retrained:",
            evidence["model_retrained"],
        )
        st.write(
            "Threshold retuned:",
            evidence["threshold_retuned"],
        )


# ============================================================
# PAGE — GOVERNANCE & SAFETY
# ============================================================

elif page == "Governance & Safety":

    st.subheader("Governance & Safety")

    st.caption(
        "Intended use, human decision authority, prohibited uses, "
        "runtime safeguards and lifecycle governance."
    )

    # ========================================================
    # GOVERNANCE & SAFETY — ENTERPRISE UI
    # ========================================================

    st.markdown(
        """
        <style>

        /* ----------------------------------------------------
           Compact metric cards
        ---------------------------------------------------- */

        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 13px 15px 12px 15px;
            min-height: 100px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.80rem;
            font-weight: 600;
            color: #475569;
            line-height: 1.2;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.35rem;
            font-weight: 650;
            color: #172B4D;
            line-height: 1.15;
        }

        /* ----------------------------------------------------
           General governance cards
        ---------------------------------------------------- */

        .gov-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 17px 19px;
            min-height: 220px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .gov-card-title {
            font-size: 1.02rem;
            font-weight: 650;
            color: #172B4D;
            margin-bottom: 12px;
            line-height: 1.25;
        }

        .gov-card-text {
            font-size: 0.88rem;
            color: #334155;
            line-height: 1.55;
        }

        .gov-card-key {
            font-weight: 650;
            color: #172B4D;
        }

        /* ----------------------------------------------------
           Runtime safety cards
        ---------------------------------------------------- */

        .safety-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 16px 18px;
            min-height: 205px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .safety-card-title {
            font-size: 1.00rem;
            font-weight: 650;
            color: #172B4D;
            margin-bottom: 11px;
            line-height: 1.25;
        }

        .safety-card-text {
            font-size: 0.87rem;
            color: #334155;
            line-height: 1.55;
        }

        .safety-card-key {
            font-weight: 650;
            color: #172B4D;
        }

        /* ----------------------------------------------------
           Section spacing
        ---------------------------------------------------- */

        div[data-testid="stHorizontalBlock"] {
            gap: 0.85rem;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOAD AUTHORITATIVE GOVERNANCE EVIDENCE
    # ========================================================

    try:
        governance_evidence = get_model_evidence()
    except Exception as exc:
        st.error(
            "Governance evidence could not be loaded from the "
            "authoritative D14 evidence artifacts."
        )
        st.exception(exc)
        st.stop()

    # ========================================================
    # GOVERNANCE STATUS
    # ========================================================

    st.markdown("### Governance Status")

    gov_col1, gov_col2, gov_col3, gov_col4 = st.columns(4)

    with gov_col1:
        st.metric(
            "Internal Validation",
            "COMPLETED",
        )

    with gov_col2:
        st.metric(
            "External Validation",
            "NOT ESTABLISHED",
        )

    with gov_col3:
        st.metric(
            "Clinical Effectiveness",
            "NOT ESTABLISHED",
        )

    with gov_col4:
        st.metric(
            "Production Deployment",
            "NOT AUTHORIZED",
        )

    st.warning(
        "RESEARCH & VALIDATION PROTOTYPE — ReadmitAI is not authorized "
        "for production clinical deployment."
    )

    # ========================================================
    # INTENDED USE & HUMAN AUTHORITY
    # ========================================================

    st.markdown("### Intended Use & Decision Authority")

    use_col1, use_col2 = st.columns(2)

    with use_col1:
        st.markdown(
            """
            <div class="gov-card">
                <div class="gov-card-title">
                    Intended Use
                </div>
                <div class="gov-card-text">
                    ReadmitAI provides
                    <span class="gov-card-key">
                        clinician-facing prioritization support
                    </span>
                    for identifying encounters that may warrant additional
                    <span class="gov-card-key">
                        30-day readmission-prevention review.
                    </span>
                    <br><br>
                    The model produces a predictive probability and a
                    governed priority signal at the frozen operating
                    threshold.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with use_col2:
        st.markdown(
            """
            <div class="gov-card">
                <div class="gov-card-title">
                    Human Decision Authority
                </div>
                <div class="gov-card-text">
                    <span class="gov-card-key">
                        Clinical judgment remains authoritative.
                    </span>
                    <br><br>
                    Model output is decision-support information only.
                    Healthcare professionals remain responsible for
                    interpretation, patient assessment and all subsequent
                    clinical decisions.
                    <br><br>
                    A model priority flag does
                    <span class="gov-card-key">not</span>
                    establish that a patient will be readmitted.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # DECISION-AUTHORITY BOUNDARY
    # ========================================================

    st.markdown("### Decision-Authority Boundary")

    authority_df = pd.DataFrame(
        {
            "Layer": [
                "Model Estimate",
                "Model Advisory",
                "Clinical Decision",
            ],
            "Function": [
                "Estimate 30-day readmission probability",
                "Prioritize encounter for additional human review",
                "Determine appropriate patient care and action",
            ],
            "Authority": [
                "Frozen AI model",
                "Governed decision-support rule",
                "Healthcare professional",
            ],
        }
    )

    st.dataframe(
        authority_df,
        hide_index=True,
        width="stretch",
    )

    st.info(
        "MODEL ESTIMATE → MODEL ADVISORY → HUMAN CLINICAL DECISION. "
        "ReadmitAI does not replace the final clinical decision-maker."
    )

    # ========================================================
    # PROHIBITED USES
    # ========================================================

    st.markdown("### Prohibited Uses")

    prohibited_col1, prohibited_col2 = st.columns(2)

    with prohibited_col1:
        st.error(
            """
            **ReadmitAI must not be used for:**

            • Autonomous discharge decisions  
            • Diagnosis of disease or clinical condition  
            • Autonomous treatment selection
            """
        )

    with prohibited_col2:
        st.error(
            """
            **ReadmitAI must not be used for:**

            • Denial or restriction of care  
            • Determining patient eligibility for care  
            • Replacement of clinician assessment
            """
        )

    # ========================================================
    # RUNTIME SAFETY CONTROLS
    # ========================================================

    st.markdown("### Runtime Safety Controls")

    safety_col1, safety_col2, safety_col3 = st.columns(3)

    with safety_col1:
        st.markdown(
            """
            <div class="safety-card">
                <div class="safety-card-title">
                    Frozen Operating Point
                </div>
                <div class="safety-card-text">
                    <span class="safety-card-key">
                        Threshold: 12.0%
                    </span>
                    <br><br>
                    Runtime inference uses the governed frozen operating
                    threshold. The application does not optimize or retune
                    the threshold.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with safety_col2:
        st.markdown(
            """
            <div class="safety-card">
                <div class="safety-card-title">
                    Zero-Utilization Safeguard
                </div>
                <div class="safety-card-text">
                    Patients with no recorded prior outpatient, emergency
                    or inpatient utilization trigger a specific
                    model-limitation warning.
                    <br><br>
                    Absence of a priority flag must not be interpreted as
                    absence of readmission risk.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with safety_col3:
        st.markdown(
            """
            <div class="safety-card">
                <div class="safety-card-title">
                    Explainability Safeguard
                </div>
                <div class="safety-card-text">
                    SHAP values describe model contribution, not clinical
                    causality.
                    <br><br>
                    Patient-level explanations must be interpreted alongside
                    the model's documented dependence on prior healthcare
                    utilization.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # OPEN GOVERNANCE RISKS
    # ========================================================

    st.markdown("### Open Governance Risks")

    risk_domains = [
        str(risk.get("risk_domain", "UNSPECIFIED"))
        .replace("_", " ")
        .title()
        for risk in governance_evidence["residual_risks"]
    ]

    risk_df = pd.DataFrame(
        {
            "Open Risk": risk_domains,
            "Status": ["OPEN"] * len(risk_domains),
        }
    )

    st.dataframe(
        risk_df,
        hide_index=True,
        width="stretch",
    )

    st.warning(
        f"{governance_evidence['unresolved_residual_risk_count']} "
        "residual risks remain unresolved. Detailed evidence, interpretation "
        "and required controls are available in the Model Evidence workspace."
    )

    # ========================================================
    # LIFECYCLE GOVERNANCE
    # ========================================================

    st.markdown("### Lifecycle Governance")

    lifecycle_col1, lifecycle_col2, lifecycle_col3 = st.columns(3)

    with lifecycle_col1:
        st.metric(
            "Candidate",
            "FROZEN",
        )

    with lifecycle_col2:
        st.metric(
            "D14 Gate Integrity",
            governance_evidence["gate_integrity_status"],
        )

    with lifecycle_col3:
        st.metric(
            "Next Governance Stage",
            "D15",
        )

    st.markdown(
        "**Governance disposition:** "
        + governance_evidence["disposition"].replace("_", " ")
    )

    st.caption(
        "No production authorization is implied by completion of internal "
        "locked-test validation. External validation, prospective workflow "
        "evaluation and clinical-effectiveness evidence remain required "
        "before future deployment consideration."
    )


# ============================================================
# PAGE — MONITORING
# ============================================================

elif page == "Monitoring":

    st.subheader("Monitoring Command Center")

    st.caption(
        "D15 deployment-monitoring design, surveillance references, "
        "escalation controls, and governance response."
    )

    # --------------------------------------------------------
    # PAGE-SPECIFIC ENTERPRISE STYLING
    # --------------------------------------------------------

    st.markdown(
        """
        <style>
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 13px 15px 11px 15px;
            min-height: 100px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.80rem;
            font-weight: 600;
            color: #475569;
            line-height: 1.25;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.35rem;
            font-weight: 600;
            color: #172B4D;
            line-height: 1.15;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 0.85rem;
        }

        .monitor-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 15px 16px;
            min-height: 178px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }

        .monitor-card-title {
            font-size: 0.98rem;
            font-weight: 650;
            color: #172B4D;
            margin-bottom: 8px;
        }

        .monitor-card-text {
            font-size: 0.86rem;
            color: #475569;
            line-height: 1.48;
        }

        .monitor-state {
            display: inline-block;
            border-radius: 999px;
            padding: 3px 9px;
            font-size: 0.72rem;
            font-weight: 700;
            margin-bottom: 9px;
        }

        .state-critical {
            background: #FEE2E2;
            color: #991B1B;
        }

        .state-alert {
            background: #FFEDD5;
            color: #9A3412;
        }

        .state-watch {
            background: #FEF3C7;
            color: #92400E;
        }

        .state-na {
            background: #E2E8F0;
            color: #475569;
        }

        .state-design {
            background: #DBEAFE;
            color: #1E40AF;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    monitoring = get_monitoring_evidence()

    # --------------------------------------------------------
    # MONITORING BOUNDARY
    # --------------------------------------------------------

    st.warning(
        "SIMULATED / DESIGN DEMONSTRATION — "
        "No live production telemetry is connected. "
        "Current production health is not assessed, and production "
        "deployment is not authorized."
    )

    # --------------------------------------------------------
    # 1. MONITORING GOVERNANCE STATUS
    # --------------------------------------------------------

    st.markdown("### Monitoring Governance Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Monitoring Controls",
            monitoring["monitoring_control_count"],
        )

    with col2:
        st.metric(
            "Escalation Triggers",
            monitoring["escalation_trigger_count"],
        )

    with col3:
        st.metric(
            "Historical Reference Bands",
            monitoring["reference_band_count"],
        )

    with col4:
        st.metric(
            "Residual Risks",
            monitoring["residual_risk_count"],
        )

    st.caption(
        f"D15 lifecycle gate: {monitoring['gate_decision']} · "
        f"Frozen model: {monitoring['registry_id']} · "
        f"Operating threshold: "
        f"{monitoring['frozen_operating_threshold']:.0%}"
    )

    # --------------------------------------------------------
    # 2. MONITORING OPERATING MODEL
    # --------------------------------------------------------

    st.markdown("### Monitoring Operating Model")

    op1, op2, op3, op4 = st.columns(4)

    with op1:
        st.markdown(
            """
            <div class="monitor-card">
                <div class="monitor-state state-design">
                    DATA & INPUTS
                </div>
                <div class="monitor-card-title">
                    Data Integrity
                </div>
                <div class="monitor-card-text">
                    Required-input completeness, schema conformance,
                    missingness, unknown categories, and input-distribution
                    surveillance.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with op2:
        st.markdown(
            """
            <div class="monitor-card">
                <div class="monitor-state state-design">
                    MODEL BEHAVIOR
                </div>
                <div class="monitor-card-title">
                    Performance Surveillance
                </div>
                <div class="monitor-card-text">
                    Prediction distribution, alert rate, discrimination,
                    calibration, and frozen operating-point performance.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with op3:
        st.markdown(
            """
            <div class="monitor-card">
                <div class="monitor-state state-design">
                    RESPONSIBLE AI
                </div>
                <div class="monitor-card-title">
                    Structural Risk
                </div>
                <div class="monitor-card-text">
                    Subgroup heterogeneity, utilization dependence,
                    admission-context behavior, and explainability
                    stability.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with op4:
        st.markdown(
            """
            <div class="monitor-card">
                <div class="monitor-state state-design">
                    CLINICAL OPERATIONS
                </div>
                <div class="monitor-card-title">
                    Human & Workflow Oversight
                </div>
                <div class="monitor-card-text">
                    Clinical override patterns, workflow adoption,
                    model-safety events, governance incidents, and
                    operational escalation.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # 3. ESCALATION ARCHITECTURE
    # --------------------------------------------------------

    st.markdown("### Escalation Architecture")

    status_counts = monitoring["escalation_status_counts"]

    esc1, esc2, esc3, esc4 = st.columns(4)

    with esc1:
        st.markdown(
            f"""
            <div class="monitor-card">
                <div class="monitor-state state-critical">
                    CRITICAL · {status_counts['CRITICAL']}
                </div>
                <div class="monitor-card-title">
                    Immediate Control Action
                </div>
                <div class="monitor-card-text">
                    Deterministic integrity or safety failures.
                    Inference is blocked where required and formal
                    escalation is activated.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with esc2:
        st.markdown(
            f"""
            <div class="monitor-card">
                <div class="monitor-state state-alert">
                    ALERT · {status_counts['ALERT']}
                </div>
                <div class="monitor-card-title">
                    Formal Governance Review
                </div>
                <div class="monitor-card-text">
                    Material evidence-dependent changes in performance,
                    calibration, subgroup behavior, utilization structure,
                    context, or explainability.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with esc3:
        st.markdown(
            f"""
            <div class="monitor-card">
                <div class="monitor-state state-watch">
                    WATCH · {status_counts['WATCH']}
                </div>
                <div class="monitor-card-title">
                    Investigation Required
                </div>
                <div class="monitor-card-text">
                    Emerging shifts in input distribution, prediction
                    behavior, alert workload, human override patterns,
                    or workflow adoption.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with esc4:
        st.markdown(
            f"""
            <div class="monitor-card">
                <div class="monitor-state state-na">
                    NOT ASSESSABLE · {status_counts['NOT_ASSESSABLE']}
                </div>
                <div class="monitor-card-title">
                    Evidence Not Mature
                </div>
                <div class="monitor-card-text">
                    Performance stability must not be inferred when
                    required outcome evidence has not matured.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.info(
        "D15 does not define a generic NORMAL state. "
        "The application therefore preserves the governed states "
        "CRITICAL, ALERT, WATCH, and NOT ASSESSABLE rather than "
        "inventing an additional status."
    )

    # --------------------------------------------------------
    # 4. INTERNAL HISTORICAL SURVEILLANCE REFERENCES
    # --------------------------------------------------------

    st.markdown("### Historical Surveillance References")

    st.caption(
        "D14 locked-test evidence carried forward into D15 as internal "
        "historical surveillance references. These values are not "
        "production acceptance limits or clinical acceptability limits."
    )

    reference_rows = []

    reference_labels = {
        "prevalence": "Prevalence",
        "alert_rate": "Alert Rate",
        "sensitivity": "Sensitivity",
        "specificity": "Specificity",
        "ppv": "PPV",
        "npv": "NPV",
    }

    for item in monitoring["reference_bands"]:

        reference_rows.append(
            {
                "Metric": reference_labels.get(
                    item["metric"],
                    item["metric"],
                ),
                "Observed": f"{item['observed_rate']:.2%}",
                "95% Reference Interval": (
                    f"{item['lower_bound']:.2%} – "
                    f"{item['upper_bound']:.2%}"
                ),
                "Events": item["events"],
                "Denominator": item["denominator"],
                "Classification": (
                    "Internal Historical Surveillance Reference"
                ),
            }
        )

    reference_display = pd.DataFrame(reference_rows)

    st.dataframe(
        reference_display,
        hide_index=True,
        width="stretch",
    )

    st.warning(
        "These historical reference intervals support surveillance "
        "comparison only. D15 explicitly does not establish production "
        "acceptance limits, clinical acceptability limits, external "
        "validation, or clinical effectiveness."
    )

    # --------------------------------------------------------
    # 5. MONITORING CONTROL REGISTER
    # --------------------------------------------------------

    st.markdown("### Monitoring Control Register")

    st.caption(
        "Authoritative D15 controls defining what must be monitored, "
        "the evidence basis, cadence, and required governance response."
    )

    control_rows = []

    for item in monitoring["monitoring_controls"]:

        risk_text = (
            ", ".join(item["d14_risk_ids"])
            if item["d14_risk_ids"]
            else "—"
        )

        control_rows.append(
            {
                "Control": item["control_id"],
                "Domain": item["domain"].replace("_", " ").title(),
                "Signal": item["signal"].replace("_", " "),
                "Reference": (
                    item["reference_type"]
                    .replace("_", " ")
                    .title()
                ),
                "Cadence": (
                    item["cadence"]
                    .replace("_", " ")
                    .title()
                ),
                "D14 Risk": risk_text,
            }
        )

    control_display = pd.DataFrame(control_rows)

    st.dataframe(
        control_display,
        hide_index=True,
        width="stretch",
    )

    # --------------------------------------------------------
    # 6. ESCALATION TRIGGER REGISTER
    # --------------------------------------------------------

    st.markdown("### Escalation Trigger Register")

    st.caption(
        "D15 governance conditions and prescribed responses. "
        "These are design controls, not claims that the trigger "
        "has occurred in production."
    )

    trigger_rows = []

    for item in monitoring["escalation_triggers"]:

        trigger_rows.append(
            {
                "Trigger": item["trigger_id"],
                "Domain": (
                    item["domain"]
                    .replace("_", " ")
                    .title()
                ),
                "Type": (
                    item["trigger_type"]
                    .replace("_", " ")
                    .title()
                ),
                "Condition": (
                    item["condition"]
                    .replace("_", " ")
                    .title()
                ),
                "State": (
                    item["status"]
                    .replace("_", " ")
                    .title()
                ),
                "Governance Action": (
                    item["action"]
                    .replace("_", " ")
                    .title()
                ),
            }
        )

    trigger_display = pd.DataFrame(trigger_rows)

    st.dataframe(
        trigger_display,
        hide_index=True,
        width="stretch",
    )

    # --------------------------------------------------------
    # 7. CURRENT EVIDENCE AVAILABILITY
    # --------------------------------------------------------

    st.markdown("### Current Evidence Availability")

    ev1, ev2, ev3, ev4 = st.columns(4)

    with ev1:
        st.metric(
            "Live Production Telemetry",
            "NOT CONNECTED",
        )

    with ev2:
        st.metric(
            "External Validation",
            "NOT ESTABLISHED",
        )

    with ev3:
        st.metric(
            "Clinical Effectiveness",
            "NOT ESTABLISHED",
        )

    with ev4:
        st.metric(
            "Production Deployment",
            "NOT AUTHORIZED",
        )

    st.error(
        "No production-health conclusion should be drawn from this "
        "Command Center. Outcome-dependent monitoring cannot be "
        "interpreted until appropriately matured prospective evidence "
        "exists."
    )

    # --------------------------------------------------------
    # 8. GOVERNANCE RESPONSE MODEL
    # --------------------------------------------------------

    st.markdown("### Governance Response Model")

    governance_response = pd.DataFrame(
        [
            {
                "State": "CRITICAL",
                "Governance Meaning":
                    "Deterministic integrity or safety failure",
                "Response":
                    "Block inference where required and activate "
                    "formal escalation / incident management",
            },
            {
                "State": "ALERT",
                "Governance Meaning":
                    "Material evidence-dependent change",
                "Response":
                    "Initiate the applicable formal governance review",
            },
            {
                "State": "WATCH",
                "Governance Meaning":
                    "Emerging surveillance signal",
                "Response":
                    "Investigate the affected data, model, workflow, "
                    "or population behavior",
            },
            {
                "State": "NOT ASSESSABLE",
                "Governance Meaning":
                    "Required evidence is not mature",
                "Response":
                    "Do not infer performance stability",
            },
        ]
    )

    st.dataframe(
        governance_response,
        hide_index=True,
        width="stretch",
    )

    # --------------------------------------------------------
    # 9. D15 TRACEABILITY
    # --------------------------------------------------------

    st.markdown("### D15 Traceability")

    st.caption(
        f"Stage: {monitoring['stage_id']} — "
        f"{monitoring['stage_name']} · "
        f"Next stage: {monitoring['next_stage']} · "
        f"Model version: {monitoring['model_version']} · "
        f"Production deployment authorized: "
        f"{monitoring['production_deployment_authorized']}"
    )

    st.caption(
        "Evidence sources: "
        f"{monitoring['manifest_source']} · "
        f"{monitoring['monitoring_control_source']} · "
        f"{monitoring['reference_band_source']} · "
        f"{monitoring['escalation_trigger_source']}"
    )

# ============================================================
# PERSISTENT FOOTER
# ============================================================

st.markdown(
    """
    <div class="readmit-footer">
        Clinical Decision Support Prototype |
        Human Oversight Required |
        Research & Validation Use Only
        <br>
        Dr. Samuel Israel, MD
    </div>
    """,
    unsafe_allow_html=True,
)