# Mapping-Teaching-Methods-and-Teaching-Tools

# 📚 Teaching Methods and Syllabus Coverage Dashboard

An interactive **Streamlit** dashboard for analyzing **teaching methods, teaching tools, faculty activities, and syllabus coverage**.
It loads attendance mapping data and syllabus coverage files, provides visual breakdowns, faculty and semester drilldowns, and highlights uncovered syllabus areas.

---

## 🚀 Features

* **Faculty, Course, and Semester Filters** – Easily drill down into specific subsets of data.
* **Teaching Method & Tool Analysis** – Bar charts with percentage distribution.
* **Faculty-wise Lecture Counts** – Compare faculty workloads visually.
* **Semester-wise Drilldowns** – Separate method/tool usage stats for each semester.
* **Syllabus Coverage Tracking** – Topic-wise subtopic coverage, pie charts, and bar charts.
* **Interactive Data View** – View filtered lecture-level data directly in the dashboard.

---

## 📂 Project Structure

```
project/
│-- Structural_Geology_Full_60_Lectures.xlsx   # Example attendance mapping file
│-- Book2.xlsx                                 # Example syllabus coverage file
│-- teaching_dashboard_fuzzy_matching.py       # Streamlit app code
│-- README.md                                  # Project documentation
```

---

## 🛠️ Steps to Run

### 1️⃣ Install Dependencies

```bash
pip install streamlit pandas seaborn matplotlib openpyxl
```

### 2️⃣ Prepare Your Input Files

#### Attendance Mapping File

Must contain the following columns:

* **faculty\_name** – Name of the faculty member.
* **course\_name** – Name of the course.
* **semester** – Semester number.
* **teaching\_method\_used** – Method used (e.g., Lecture, Group Discussion).
* **teaching\_tool\_used** – Tool used (e.g., PPT, Book & Pen).
* **topic\_covered** – Lecture topic covered.

#### Syllabus Coverage File

Must contain the following columns:

* **Topic** – Main syllabus topic.
* **Subtopic** – Subtopic name.
* **Status** – Covered / Not Covered.

Example files:

* `Structural_Geology_Full_60_Lectures.xlsx`
* `Book2.xlsx`

---

### 3️⃣ Run the App

```bash
streamlit run teaching_dashboard_fuzzy_matching.py
```

---

### 4️⃣ Use the Dashboard

* **Step 1:** Upload the attendance mapping file.
* **Step 2:** Apply filters from the sidebar (Faculty, Course, Semester, Method, Tool).
* **Step 3:** View:

  * Total lectures, faculty count, and course count.
  * Teaching method and tool usage charts.
  * Faculty-wise lecture distribution.
  * Semester-wise teaching trends.
* **Step 4:** Upload the syllabus coverage file to see:

  * Topic-wise subtopic coverage table.
  * Pie charts showing covered vs not covered subtopics.
  * Bar chart showing % coverage for each topic.

---


## 🌐 Live App

https://mapping-teaching-methods-and-teaching-tools.streamlit.app/
