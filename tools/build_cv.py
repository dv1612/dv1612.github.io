"""
build_cv.py
-----------
Renders assets/Dhruvi-Vegda-CV.pdf from the same content as the LaTeX resume,
so the site's "Download CV" button always has a file to serve.

Usage:  python tools/build_cv.py
"""

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

NAVY = colors.HexColor("#1f3864")
INK = colors.HexColor("#1a1a1a")
INK_2 = colors.HexColor("#3c4452")
MUTED = colors.HexColor("#6b7280")
RULE = colors.HexColor("#d6dbe4")
LINK = colors.HexColor("#1155cc")

PAGE_W, PAGE_H = A4
MARGIN = 15 * mm

S = {
    "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=22, leading=25,
                           textColor=NAVY, alignment=1, spaceAfter=4),
    "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.6, leading=12,
                              textColor=INK_2, alignment=1, spaceAfter=2),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.8, leading=13,
                         textColor=NAVY, spaceBefore=9, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=8.9, leading=12.2,
                           textColor=INK_2, alignment=TA_JUSTIFY),
    "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=9.6, leading=12,
                           textColor=INK),
    "org": ParagraphStyle("org", fontName="Helvetica-Oblique", fontSize=8.8, leading=11,
                          textColor=MUTED, spaceAfter=2),
    "date": ParagraphStyle("date", fontName="Helvetica", fontSize=8.4, leading=12,
                           textColor=MUTED, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=8.9, leading=12.2,
                             textColor=INK_2, leftIndent=9, bulletIndent=1, spaceAfter=1.5),
}


def rule():
    t = Table([[""]], colWidths=[PAGE_W - 2 * MARGIN], rowHeights=[1.1])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return t


def heading(text):
    return KeepTogether([Paragraph(text.upper(), S["h2"]),
                         Table([[""]], colWidths=[PAGE_W - 2 * MARGIN], rowHeights=[0.7],
                               style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), RULE),
                                                 ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                                 ("TOPPADDING", (0, 0), (-1, -1), 0),
                                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 3)])),
                         Spacer(1, 4)])


def entry(role, org, date, bullets):
    width = PAGE_W - 2 * MARGIN
    head = Table([[Paragraph(role, S["role"]), Paragraph(date, S["date"])]],
                 colWidths=[width * 0.74, width * 0.26],
                 style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                   ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                   ("TOPPADDING", (0, 0), (-1, -1), 0),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    flow = [head, Paragraph(org, S["org"])]
    flow += [Paragraph(b, S["bullet"], bulletText="•") for b in bullets]
    flow.append(Spacer(1, 5))
    return KeepTogether(flow)


def build(out: Path) -> int:
    story = [
        Paragraph("DHRUVI VEGDA", S["name"]),
        Paragraph(
            'Bengaluru, India &nbsp;|&nbsp; +91 94295 34902 &nbsp;|&nbsp; '
            '<a href="mailto:dhruvivegda2501@gmail.com"><font color="#1155cc">'
            'dhruvivegda2501@gmail.com</font></a> &nbsp;|&nbsp; '
            '<a href="https://www.linkedin.com/in/dhruvi-vegda-dv1612"><font color="#1155cc">LinkedIn</font></a>'
            ' &nbsp;|&nbsp; <a href="https://github.com/dv1612"><font color="#1155cc">GitHub</font></a>'
            ' &nbsp;|&nbsp; <a href="https://dv1612.github.io"><font color="#1155cc">Portfolio</font></a>',
            S["contact"]),
        Spacer(1, 5), rule(), Spacer(1, 2),

        heading("Professional Summary"),
        Paragraph(
            "Business Analyst and Power BI professional with commercial experience building automated "
            "Power BI reports and dashboards using DAX, Power Query and SQL. Experienced across data "
            "extraction, transformation, cleansing, validation and analysis of operational datasets, "
            "translating business requirements into KPI reporting and scalable BI solutions. Strong "
            "foundation in data modelling, ETL, the Microsoft Power Platform and advanced Excel, "
            "partnering with cross-functional stakeholders to improve reporting efficiency, data "
            "accuracy and decision-making.", S["body"]),

        heading("Technical Skills"),
        Paragraph("<b>Business Intelligence:</b> Power BI, DAX, Power Query, KPI reporting, data visualization, report automation", S["body"]),
        Paragraph("<b>Data &amp; Databases:</b> SQL (MySQL, PostgreSQL), CTEs, window functions, ETL, data cleansing, validation", S["body"]),
        Paragraph("<b>Data Modelling:</b> Star schema, fact &amp; dimension design, relationship design, Power BI modelling", S["body"]),
        Paragraph("<b>Programming:</b> Python (Pandas, NumPy, Matplotlib, Seaborn), SPSS", S["body"]),
        Paragraph("<b>Power Platform:</b> Power Apps, Power Automate, approval workflows", S["body"]),
        Paragraph("<b>Analytics &amp; Reporting:</b> Advanced Excel, pivot tables, statistical analysis, forecasting", S["body"]),

        heading("Work Experience"),
        entry("Business Analyst", "Adani Enterprises Ltd.", "May 2026 &ndash; Present", [
            "Engineered 5+ automated Power BI dashboards using DAX and Power Query to centralize enterprise "
            "data, reducing manual reporting time by 15% and providing real-time KPIs for 20+ stakeholders.",
            "Analyzed cross-functional project data using SQL and Excel, identifying operational bottlenecks "
            "and delivering visual insights that improved project tracking accuracy.",
        ]),
        entry("Business Analyst Intern", "Adani Enterprises Ltd.", "Oct 2025 &ndash; Apr 2026", [
            "Led data analysis for the Hunger Box application deployment, using SQL to extract usage metrics "
            "and inform cafeteria capacity planning.",
            "Coordinated with 3 internal teams to resolve implementation issues, maintaining 99% system "
            "uptime through the pilot phase.",
        ]),
        entry("Power Platform Developer", "Adani Power Ltd.", "Jan 2025 &ndash; Apr 2025", [
            "Designed and deployed PRAVIX in Microsoft Power Apps to automate APM user access requests, "
            "cutting request turnaround time by 30%.",
            "Configured multi-level approval workflows and automated notifications, with SOPs for "
            "standardized operational compliance.",
        ]),
        entry("Sales Executive", "Dabur Ltd.", "Jan 2023 &ndash; Feb 2023", [
            "Used historical sales data and customer analytics to optimize retail supermarket interactions, "
            "contributing to enhanced consumer engagement.",
        ]),

        heading("Data &amp; Analytics Projects"),
        entry('E-Commerce Customer Segmentation (RFM) &nbsp;|&nbsp; Python &middot; SQL &middot; Power BI &nbsp;'
              '<a href="https://github.com/dv1612/ecommerce-customer-segmentation">'
              '<font color="#1155cc" size="7.5">[code]</font></a>', "", "Sep 2026", [
            "Cleaned 541,909 retail transactions to 392,692 valid rows in Pandas, then scored every customer "
            "in PostgreSQL using CTEs and NTILE(5) window functions.",
            "Segmented 4,338 customers into 11 segments, quantifying that 20% of customers drive 64% of "
            "revenue and that 646 lapsing accounts hold &pound;1.03M of historic spend.",
            "Delivered the Power BI layer: a SWITCH(TRUE()) segmentation column plus revenue, customer and "
            "AOV measures.",
        ]),
        entry('SaaS Subscription Funnel &amp; Churn Analysis &nbsp;|&nbsp; Python &middot; SQL &middot; Power BI &nbsp;'
              '<a href="https://github.com/dv1612/saas-subscription-funnel-churn">'
              '<font color="#1155cc" size="7.5">[code]</font></a>', "", "Jun 2026", [
            "Instrumented a four-stage funnel from 66,000 raw event logs, isolating a single step losing 57% "
            "of users.",
            "Modelled cohort retention and MRR movement in PostgreSQL using generate_series, showing 62% of "
            "cancellations occur within three months and shifting budget from win-back to onboarding.",
            "Built DAX measures for churn rate, retention rate, active and lost MRR and net revenue retention.",
        ]),
        entry('Retail Inventory &amp; Margin Optimization &nbsp;|&nbsp; Python &middot; SQL &middot; Power BI &nbsp;'
              '<a href="https://github.com/dv1612/retail-inventory-margin-optimization">'
              '<font color="#1155cc" size="7.5">[code]</font></a>', "", "Mar 2026", [
            "Standardized a 6,220-row warehouse extract with four SKU formats, missing costs and negative "
            "counts, merging it with the product master to derive margin percentage per SKU.",
            "Computed daily sales velocity, days of supply and ABC class across 1,200 SKUs and 5 warehouses, "
            "flagging 234 SKUs carrying &pound;1,786/day of gross margin at stockout risk.",
            "Identified 174 shortages resolvable by inter-warehouse transfer instead of purchase orders.",
        ]),
        entry("Rural Gujarat Response to SDG 6 (Research Paper)", "", "Jan &ndash; Dec 2023", [
            "Analyzed primary survey data from 400+ respondents across 5 villages using SPSS and Excel "
            "against 20+ water, sanitation and hygiene KPIs.",
            "Delivered recommendations to the Gandhinagar Municipal Corporation to improve resource "
            "accessibility and operational outcomes.",
        ]),

        heading("Education"),
        entry("PGDM in Big Data Analytics",
              "Adani Institute of Digital Technology Management (AIDTM) &nbsp;|&nbsp; CGPA 3.59/4.33",
              "Jul 2024 &ndash; Apr 2026", []),
        entry("BBA (Hons.) in Marketing",
              "Pandit Deendayal Energy University (PDEU) &nbsp;|&nbsp; CGPA 9.50/10",
              "Aug 2020 &ndash; May 2024", []),

        heading("Achievements &amp; Leadership"),
        Paragraph("<b>Liaison Officer</b> &mdash; coordinated logistics and delegation support at the G20 "
                  "Mayoral Summit for Mr. Sanjeev Sanyal.", S["bullet"], bulletText="•"),
        Paragraph("<b>Publicity Head</b> &mdash; managed communications for 'The Inspired Room' "
                  "architectural club at PDEU.", S["bullet"], bulletText="•"),
        Paragraph("<b>Athletics</b> &mdash; state-level baseball player; teamwork, discipline and "
                  "performance under pressure.", S["bullet"], bulletText="•"),
    ]

    doc = BaseDocTemplate(str(out), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN, bottomMargin=MARGIN,
                          title="Dhruvi Vegda - CV", author="Dhruvi Vegda",
                          subject="Business Analyst / Power BI Developer")
    frame = Frame(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="cv", frames=[frame])])
    doc.build(story)
    print(f"  {out}  ({out.stat().st_size / 1024:.0f} KB, {doc.page} pages)")
    return 0


if __name__ == "__main__":
    target = Path(__file__).resolve().parent.parent / "assets" / "Dhruvi-Vegda-CV.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    sys.exit(build(target))
