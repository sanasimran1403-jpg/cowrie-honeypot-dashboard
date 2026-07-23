from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from parse_data import get_dashboard_data
from datetime import datetime

data = get_dashboard_data()

# ---- Theme colors ----
BG = colors.HexColor("#0b1120")
PANEL = colors.HexColor("#131c2e")
ROW_ALT = colors.HexColor("#0f1729")
BORDER = colors.HexColor("#2a3550")
ACCENT = colors.HexColor("#00e5a0")
MUTED = colors.HexColor("#8b98ac")
WHITE = colors.HexColor("#e6edf3")
DANGER = colors.HexColor("#ff4d6d")

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=20, textColor=WHITE, alignment=TA_CENTER, spaceAfter=4)
sub_style = ParagraphStyle('Sub', fontName='Helvetica', fontSize=9, textColor=MUTED, alignment=TA_CENTER, spaceAfter=14)
heading_style = ParagraphStyle('Heading', fontName='Helvetica-Bold', fontSize=12, textColor=WHITE, spaceBefore=16, spaceAfter=8)
body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=9.5, textColor=WHITE, leading=14)
status_big = ParagraphStyle('StatusBig', fontName='Helvetica-Bold', fontSize=26, textColor=ACCENT, alignment=TA_CENTER)
status_sub = ParagraphStyle('StatusSub', fontName='Helvetica', fontSize=9, textColor=MUTED, alignment=TA_CENTER)

# ---- Background + watermark + footer on every page ----
def draw_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    # watermark logo, centered, faded
    try:
        canvas.saveState()
        canvas.translate(A4[0]/2, A4[1]/2)
        canvas.setFillAlpha(0.06)
        logo_w, logo_h = 10*cm, 10*cm
        canvas.drawImage("logo.png", -logo_w/2, -logo_h/2, width=logo_w, height=logo_h,
                          mask='auto', preserveAspectRatio=True)
        canvas.restoreState()
    except Exception:
        pass

    # footer
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, 1.5*cm, A4[0]-2*cm, 1.5*cm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(2*cm, 1*cm, "S&S  |  Honeypot Threat Intelligence Report")
    canvas.drawRightString(A4[0]-2*cm, 1*cm, f"Page {doc.page}")
    canvas.restoreState()

def styled_table(table_data, col_widths, header=True):
    style = [
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
    ]
    for i in range(1 if header else 0, len(table_data)):
        bg = ROW_ALT if i % 2 == (1 if header else 0) else PANEL
        style.append(('BACKGROUND', (0,i), (-1,i), bg))
    if header:
        style.append(('BACKGROUND', (0,0), (-1,0), PANEL))
        style.append(('TEXTCOLOR', (0,0), (-1,0), ACCENT))
        style.append(('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'))
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle(style))
    return t

doc = SimpleDocTemplate("honeypot_report.pdf", pagesize=A4,
                        topMargin=2*cm, bottomMargin=2*cm,
                        leftMargin=2*cm, rightMargin=2*cm)

elements = []

logo = Image("logo.png", width=1.6*cm, height=1.6*cm)
header_title = Paragraph("Honeypot Threat Intelligence Report", ParagraphStyle('HT', fontName='Helvetica-Bold', fontSize=16, textColor=WHITE))
header_sub = Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M UTC')}", ParagraphStyle('HS', fontName='Helvetica', fontSize=8.5, textColor=MUTED))
header_table = Table([[logo, [header_title, header_sub]]], colWidths=[2.2*cm, 13.8*cm])
header_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
elements.append(header_table)
elements.append(Spacer(1, 10))
elements.append(Table([['']], colWidths=[16*cm], style=TableStyle([('LINEBELOW', (0,0), (-1,-1), 1, BORDER)])))
elements.append(Spacer(1, 16))

# ---- Status box ----
risk_note = "Automated attacker traffic captured on a controlled honeypot sensor."
status_box = Table([
    [Paragraph("ACTIVE SENSOR", status_big)],
    [Paragraph(f"Sessions Logged: <b>{data['total_sessions']}</b> &nbsp;|&nbsp; Unique Usernames: <b>{len(data['top_usernames'])}</b> &nbsp;|&nbsp; Payload Fetches: <b>{len(data['downloads'])}</b>", status_sub)],
], colWidths=[16*cm])
status_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), PANEL),
    ('BOX', (0,0), (-1,-1), 1, ACCENT),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
]))
elements.append(status_box)
elements.append(Spacer(1, 10))

elements.append(Paragraph(
    "This report summarizes attacker behavior captured by a self-hosted Cowrie SSH/Telnet "
    "honeypot deployed for security research purposes. The honeypot simulates a vulnerable "
    "Linux server to observe brute-force login patterns, command execution attempts, and "
    "malware download behavior.", body_style))

elements.append(Paragraph("■  Top Attempted Usernames", heading_style))
uname_data = [["Username", "Attempts"]] + [[u, str(c)] for u, c in data["top_usernames"]]
elements.append(styled_table(uname_data, [11*cm, 5*cm]))

elements.append(Paragraph("■  Top Attempted Passwords", heading_style))
pw_data = [["Password", "Attempts"]] + [[p, str(c)] for p, c in data["top_passwords"]]
elements.append(styled_table(pw_data, [11*cm, 5*cm]))

elements.append(Paragraph("■  Top Username / Password Combinations", heading_style))
combo_data = [["Combination", "Attempts"]] + [[c, str(n)] for c, n in data["top_combos"]]
elements.append(styled_table(combo_data, [11*cm, 5*cm]))

elements.append(Paragraph("■  MITRE ATT&CK Mapping", heading_style))
mitre_data = [
    ["Technique ID", "Technique Name", "Observed Behavior"],
    ["T1110", "Brute Force", "Repeated login attempts with common credential pairs"],
    ["T1078", "Valid Accounts", "Successful fake logins using weak/default credentials"],
    ["T1105", "Ingress Tool Transfer", "wget/curl attempts to fetch external payloads"],
    ["T1082", "System Information Discovery", "Commands like uname -a, cat /etc/passwd"],
]
elements.append(styled_table(mitre_data, [3*cm, 5*cm, 8*cm]))

elements.append(Paragraph("■  Conclusion", heading_style))
elements.append(Paragraph(
    "The captured data confirms common automated attack patterns targeting SSH services — "
    "primarily credential-stuffing attempts using default and weak passwords across common "
    "usernames (root, admin, ubuntu, test, user). This aligns with real-world internet-wide "
    "scanning behavior and highlights the importance of disabling password authentication, "
    "enforcing key-based SSH access, and monitoring for repeated failed login attempts.", body_style))

doc.build(elements, onFirstPage=draw_background, onLaterPages=draw_background)
print("Report generated: honeypot_report.pdf")
