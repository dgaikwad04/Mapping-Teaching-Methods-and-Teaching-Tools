import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from difflib import get_close_matches

st.set_page_config(page_title="Teaching Dashboard", layout="wide")
st.title("📚 Teaching Methods and Syllabus Coverage Dashboard")

# === Sidebar Uploads ===
st.sidebar.markdown("### 📁 Upload Attendance Mapping Excel File")
data_file = st.sidebar.file_uploader("Upload Excel file", type=["xlsx", "csv"], key="data_file")

st.sidebar.markdown("### 📘 Upload Syllabus Coverage File")
syllabus_file = st.sidebar.file_uploader("Upload Excel or CSV with columns: Topic, Subtopic, Status", type=["xlsx", "csv"], key="syllabus_file")

# === Load Attendance Data ===
if data_file:
    df = pd.read_csv(data_file) if data_file.name.endswith(".csv") else pd.read_excel(data_file)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.rename(columns={
        "course_title": "course_name",
        "teaching_method": "teaching_method_used",
        "tools_used": "teaching_tool_used",
        "faculty": "faculty_name"
    })

    required_columns = ["faculty_name", "course_name", "semester", "teaching_method_used", "teaching_tool_used", "topic_covered"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        st.error(f"❌ Missing required columns in Excel file: {missing}")
        st.stop()

    # === Filters ===
    st.sidebar.title("🔍 Filters")
    faculty = st.sidebar.multiselect("👩‍🏫 Select Faculty", df['faculty_name'].unique(), default=df['faculty_name'].unique())
    course = st.sidebar.multiselect("📚 Select Course", df['course_name'].unique(), default=df['course_name'].unique())
    semester = st.sidebar.multiselect("🎓 Select Semester", sorted(df['semester'].unique()), default=sorted(df['semester'].unique()))
    method = st.sidebar.multiselect("🧠 Teaching Method", df['teaching_method_used'].unique(), default=df['teaching_method_used'].unique())
    tool = st.sidebar.multiselect("🛠️ Teaching Tool", df['teaching_tool_used'].unique(), default=df['teaching_tool_used'].unique())

    filtered_df = df[
        (df['faculty_name'].isin(faculty)) &
        (df['course_name'].isin(course)) &
        (df['semester'].isin(semester)) &
        (df['teaching_method_used'].isin(method)) &
        (df['teaching_tool_used'].isin(tool))
    ]

    # === KPIs ===
    st.subheader("📊 Teaching Dashboard Overview")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Lectures", len(filtered_df))
    kpi2.metric("Unique Faculty", filtered_df['faculty_name'].nunique())
    kpi3.metric("Unique Courses", filtered_df['course_name'].nunique())

    # === Teaching Method & Tool Visuals ===
    st.markdown("### 📈 Visualizations")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Teaching Methods Distribution**")
        method_counts = filtered_df['teaching_method_used'].value_counts()
        total = method_counts.sum()
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        method_counts.plot(kind='barh', ax=ax1, color='skyblue')
        for i, v in enumerate(method_counts):
            percent = f"{(v/total)*100:.1f}%"
            ax1.text(v + 0.5, i, f"{v} ({percent})", va='center', fontsize=9)
        ax1.set_xlabel("Count")
        ax1.set_xlim([0, method_counts.max() * 1.3])
        st.pyplot(fig1)

    with col2:
        st.markdown("**Teaching Tools Distribution**")
        tool_counts = filtered_df['teaching_tool_used'].value_counts()
        total = tool_counts.sum()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        tool_counts.plot(kind='barh', ax=ax2, color='salmon')
        for i, v in enumerate(tool_counts):
            percent = f"{(v/total)*100:.1f}%"
            ax2.text(v + 0.5, i, f"{v} ({percent})", va='center', fontsize=9)
        ax2.set_xlabel("Count")
        ax2.set_xlim([0, tool_counts.max() * 1.3])
        st.pyplot(fig2)

    # === Faculty Breakdown ===
    st.markdown("### 👩‍🏫 Faculty-wise Lecture Count")
    faculty_counts = filtered_df['faculty_name'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.barplot(x=faculty_counts.values, y=faculty_counts.index, palette='Blues_d', ax=ax3)
    total = faculty_counts.sum()
    for i, v in enumerate(faculty_counts.values):
        percent = f"{(v/total)*100:.1f}%"
        ax3.text(v + 0.5, i, f"{v} ({percent})", va='center')
    ax3.set_xlabel("Lectures")
    ax3.set_xlim([0, faculty_counts.max() * 1.3])
    st.pyplot(fig3)

    # === Semester-wise Drilldown ===
    st.markdown("### 🌟 Semester-wise Drilldown: Teaching Methods and Tools")
    for sem in sorted(filtered_df['semester'].unique()):
        st.markdown(f"#### 📘 Semester {sem}")
        sem_df = filtered_df[filtered_df['semester'] == sem]
        colA, colB = st.columns(2)

        with colA:
            st.markdown("##### 📊 Teaching Methods Used")
            method_counts = sem_df['teaching_method_used'].value_counts()
            figA, axA = plt.subplots(figsize=(5, 4))
            sns.barplot(x=method_counts.index, y=method_counts.values, palette='Set2', ax=axA)
            total = method_counts.sum()
            for i, v in enumerate(method_counts.values):
                percent = f"{(v/total)*100:.1f}%"
                axA.text(i, v + 0.5, f"{v}\n({percent})", ha='center', va='bottom', fontsize=9)
            axA.set_ylabel("Lecture Count")
            axA.set_xlabel("Method")
            axA.set_ylim([0, method_counts.max() * 1.4])
            plt.xticks(rotation=30, ha='right')
            st.pyplot(figA)

        with colB:
            st.markdown("##### 🛠️ Teaching Tools Used")
            tool_counts = sem_df['teaching_tool_used'].value_counts()
            figB, axB = plt.subplots(figsize=(5, 4))
            sns.barplot(x=tool_counts.index, y=tool_counts.values, palette='Set3', ax=axB)
            total = tool_counts.sum()
            for i, v in enumerate(tool_counts.values):
                percent = f"{(v/total)*100:.1f}%"
                axB.text(i, v + 0.5, f"{v}\n({percent})", ha='center', va='bottom', fontsize=9)
            axB.set_ylabel("Lecture Count")
            axB.set_xlabel("Tool")
            axB.set_ylim([0, tool_counts.max() * 1.4])
            plt.xticks(rotation=30, ha='right')
            st.pyplot(figB)

    st.markdown("### 📋 Filtered Lecture Data")
    st.dataframe(filtered_df)

# === Load Syllabus Status Data ===
if syllabus_file:
    s_df = pd.read_csv(syllabus_file) if syllabus_file.name.endswith(".csv") else pd.read_excel(syllabus_file)
    s_df.columns = s_df.columns.str.strip().str.lower()
    if not {"topic", "subtopic", "status"}.issubset(s_df.columns):
        st.error("❌ File must include 'Topic', 'Subtopic', and 'Status' columns.")
    else:
        s_df["status"] = s_df["status"].str.strip().str.lower()
        report = []
        for topic, group in s_df.groupby("topic"):
            covered = group[group["status"] == "covered"]
            not_covered = group[group["status"] == "not covered"]
            total = len(group)
            percent = round(len(covered) / total * 100, 2) if total else 0
            report.append({
                "Topic": topic,
                "Total Subtopics": total,
                "Covered": len(covered),
                "Not Covered": len(not_covered),
                "% Covered": percent,
                "Covered Subtopics": covered["subtopic"].tolist(),
                "Not Covered Subtopics": not_covered["subtopic"].tolist()
            })

        report_df = pd.DataFrame(report)
        st.markdown("### 🧾 Topic-wise Subtopic Coverage Summary")
        st.dataframe(report_df[["Topic", "Total Subtopics", "Covered", "Not Covered", "% Covered"]])

        st.markdown("### 🥧 Topic-wise Coverage Pie Charts")
        for i in range(0, len(report_df), 2):
            pie_cols = st.columns(2)
            for j in range(2):
                if i + j < len(report_df):
                    topic = report_df.iloc[i + j]
                    pie_data = [topic["Covered"], topic["Not Covered"]]
                    pie_labels = ["Covered", "Not Covered"]
                    fig, ax = plt.subplots(figsize=(4, 4))
                    ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=["#66bb6a", "#ef5350"])
                    ax.set_title(f"{topic['Topic']} ({topic['% Covered']}%)")
                    pie_cols[j].pyplot(fig)

        st.markdown("### 📊 Topic-wise % Coverage Bar Chart")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=report_df, x="Topic", y="% Covered", palette="Greens_d", ax=ax)
        for index, row in report_df.iterrows():
            ax.text(index, row["% Covered"] + 1, f"{row['% Covered']}%", ha='center')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
else:
    st.info("📄 Upload Valid Files to Continue.")
