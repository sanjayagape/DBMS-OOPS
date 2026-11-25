from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile, ZIP_DEFLATED
from hashlib import sha256
import json, math
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(r'E:\Projects\DBMS OOPS\review')
TMP=ROOT/'.build'
REF=Path(r'C:\Users\HOME\Downloads\EMPLOYEE DETAILS AND PAYROLL MANAGEMENT SYSTEM (2)-3 (1).docx')
OUT=ROOT/'FoodBridge_Project_Review.docx'
ROOT.mkdir(parents=True,exist_ok=True)
digest=sha256(REF.read_bytes()).hexdigest()
source=Document(REF)
original_paras=list(source.paragraphs)
logo_bytes=source.part.related_parts['rId7'].blob
(TMP/'college-logo.png').write_bytes(logo_bytes)
inventory={}
with ZipFile(REF) as z:
    inventory={n:{'bytes':len(z.read(n)),'sha256':sha256(z.read(n)).hexdigest()} for n in z.namelist()}
(TMP/'reference_inventory.json').write_text(json.dumps(inventory,indent=2))
(TMP/'artifact.md').write_text(f'''# FoodBridge review template contract
Reference: {REF}
SHA256: {digest}
Reference render: .build/reference.pdf and reference-render/page-01.png through page-42.png
Reference has 42 rendered pages and 44 section definitions. All page patterns inspected.
Page system: portrait US Letter 8.5 by 11 inches, 0.75 inch side margins, baseline 0.958333 inch top and 0.833333 inch bottom. Source variations in top margins only support code pagination.
Typography: Times New Roman. Cover title and team names bold 14 pt centered, subtitle bold 14 pt, body 12 pt justified, abstract 13 pt, chapter title bold 18 pt, subsection bold 14 pt. Source uses black text and white pages. Cover college logo retained with original proportions. Footer page number at right.
Ordered slots: cover, certificate, abstract, contents, introduction, functionalities, system flow, data flow, use cases, ERD, module descriptions, implementation, conclusion, references.
Stable locations: document.xml body paragraphs 0 to 25 cover, 26 to 57 certificate, 58 abstract heading, 60 abstract body, 62 contents heading, 70 chapter role, 72 subsection role, 75 body role, 101 list role, 162 implementation heading. Diagram/screenshot slots occur in chapter 3 and chapter 5.
Editable: body content, team metadata, TOC page entries, diagram assets, document relationships for new assets, footer and properties. Retain source styles, numbering, theme, font tables, original images and all other opaque package members byte-for-byte. See reference_inventory.json for every package part.
Creation: load the retained reference, clone its paragraph components, replace obsolete body content. Copy source logo paragraph with its relationship. New diagram slots use black outlined figures with labelled connectors. Implementation uses illustrative Java/SQL and planned verification, without completion claims or screenshots.
Pagination: clone the source page geometry and footer treatment. Replace source section breaks used for long payroll code with explicit page breaks for a shorter 20-page FoodBridge review. The user requested the format, not the original page count. Preserve body and heading size rather than shrinking to fit. Final section count deliberately becomes one.
Team: Sanjay P 251501200; Mohammed Shaahid Ahmed 251501136; BarathKumar S 251501030; Nitish S 251501157. Use latest user spellings. College confirmed as Rajalakshmi Engineering College. Department and faculty fields stay editable placeholders. No invented signatures or test results.
Fidelity gates: original reference hash unchanged, preserve-only package parts unchanged, original logo unchanged, chapter order matches, every final page inspected after Word PDF export. Packaged render_docx.py attempted and failed because LibreOffice unavailable, so use installed Word PDF exporter and bundled Poppler as fallback. Do not modify reference.
''',encoding='utf-8')

# Diagrams are deterministic technical figures, not application screenshots.
font_path=r'C:\Windows\Fonts\arial.ttf'
bold_path=r'C:\Windows\Fonts\arialbd.ttf'
def canvas(h=1000):
    im=Image.new('RGB',(1500,h),'white'); return im,ImageDraw.Draw(im)
def f(size=30,bold=False): return ImageFont.truetype(bold_path if bold else font_path,size)
def label(draw,xy,txt,size=30,bold=False,anchor='mm'):
    draw.multiline_text(xy,txt,font=f(size,bold),fill='black',anchor=anchor,align='center',spacing=9)
def box(draw,rect,txt,size=30,ellipse=False):
    (draw.ellipse if ellipse else draw.rectangle)(rect,outline='black',width=3)
    label(draw,((rect[0]+rect[2])/2,(rect[1]+rect[3])/2),txt,size)
def arrow(draw,points,txt=None,at=None):
    draw.line(points,fill='black',width=3)
    a,b=points[-2],points[-1]; ang=math.atan2(b[1]-a[1],b[0]-a[0]); L=17
    draw.polygon([b,(b[0]-L*math.cos(ang-.45),b[1]-L*math.sin(ang-.45)),(b[0]-L*math.cos(ang+.45),b[1]-L*math.sin(ang+.45))],fill='black')
    if txt: label(draw,at,txt,25)
im,dr=canvas(1050)
stages=['Register and log in','Donor publishes food details','NGO claims available food','Volunteer accepts pickup','Collect and confirm delivery','Record donation history and impact']
for i,t in enumerate(stages):
    y=25+i*165; box(dr,(300,y,1200,y+100),t,32)
    if i<5: arrow(dr,[(750,y+100),(750,y+160)])
im.save(TMP/'flow.png')
im,dr=canvas(1100)
box(dr,(15,100,340,250),'DONOR',34)
box(dr,(565,100,950,250),'1.0 Manage\ndonations',32)
box(dr,(1170,100,1485,250),'D1 Donations',29)
arrow(dr,[(340,175),(565,175)],'Food details',(450,130))
arrow(dr,[(950,175),(1170,175)],'Save',(1055,130))
box(dr,(15,450,340,600),'NGO',34)
box(dr,(565,450,950,600),'2.0 Claim\ndonation',32)
box(dr,(1170,450,1485,600),'D2 Claims',29)
arrow(dr,[(340,525),(565,525)],'Claim request',(450,480))
arrow(dr,[(950,525),(1170,525)],'Save claim',(1060,480))
arrow(dr,[(1325,250),(1325,330),(760,330),(760,450)],'Availability',(1030,292))
box(dr,(15,850,340,1000),'VOLUNTEER',32)
box(dr,(565,850,950,1000),'3.0 Track pickup\nand delivery',31)
box(dr,(1170,850,1485,1000),'D3 Pickups and\ndelivery records',28)
arrow(dr,[(340,925),(565,925)],'Status update',(450,880))
arrow(dr,[(950,925),(1170,925)],'Save progress',(1060,880))
arrow(dr,[(1325,600),(1325,700),(760,700),(760,850)],'Confirmed claim',(1030,660))
im.save(TMP/'dfd.png')
im,dr=canvas(1100)
dr.rectangle((440,20,1480,1070),outline='black',width=3)
label(dr,(960,60),'FOODBRIDGE',32,True)
actors=[('Donor',190),('NGO',400),('Volunteer',610),('Admin',820),('Citizen',1010)]
uses=['Post and manage donations','Browse and claim food','Accept pickup and update delivery','Verify users and manage platform','View community activity and impact']
for (a,y),u in zip(actors,uses):
    box(dr,(30,y-40,300,y+40),a,32)
    box(dr,(610,y-62,1390,y+62),u,29,True)
    dr.line([(300,y),(610,y)],fill='black',width=3)
im.save(TMP/'usecase.png')
im,dr=canvas(1300)
ents=[((40,30,620,230),'USERS\nPK user_id\nname, email, primary_role'),((880,30,1460,230),'ORGANIZATIONS\nPK organization_id\nname, verification_status'),((40,400,620,620),'FOOD DONATIONS\nPK donation_id   FK donor_id\nquantity, status, pickup_deadline'),((880,400,1460,620),'DONATION CLAIMS\nPK claim_id   FK donation_id UNIQUE\nFK organization_id, claimed_by_user_id'),((880,820,1460,1020),'PICKUPS\nPK pickup_id   FK claim_id UNIQUE\nFK volunteer_id, status'),((40,820,620,1020),'DELIVERY RECORDS\nPK delivery_id   FK pickup_id UNIQUE\ndelivered_at, confirmed_by_user_id')]
for rect,t in ents: box(dr,rect,t,27)
arrow(dr,[(330,230),(330,400)],'1 to many',(450,310))
arrow(dr,[(1170,230),(1170,400)],'1 to many',(1300,310))
arrow(dr,[(620,510),(880,510)],'1 to 0..1',(750,465))
arrow(dr,[(1170,620),(1170,820)],'1 to 0..1',(1300,720))
arrow(dr,[(880,920),(620,920)],'1 to 0..1',(750,875))
label(dr,(750,1150),'PK = primary key   FK = foreign key\nA user can also act as the assigned volunteer or claim creator.',28)
im.save(TMP/'erd.png')

doc=Document(REF)
body=doc._element.body
base_sect=deepcopy(doc.sections[0]._sectPr)
for child in list(body): body.remove(child)
body.append(base_sect)
# Keep the source footer relationship and continuous page numbering.
for el in base_sect.findall(qn('w:pgNumType')): base_sect.remove(el)
def para(txt='',role='body',center=False,bold=None,size=None,before=None,after=None):
    idx={'body':75,'chapter':70,'sub':72,'cover':0,'list':101}.get(role,75)
    template=deepcopy(original_paras[idx]._p)
    for child in list(template):
        if child.tag!=qn('w:pPr'): template.remove(child)
    pp=template.find(qn('w:pPr'))
    if pp is not None:
        for child in list(pp):
            if child.tag in [qn('w:sectPr'),qn('w:numPr'),qn('w:pageBreakBefore')]: pp.remove(child)
    body.insert(len(body)-1,template)
    from docx.text.paragraph import Paragraph
    p=Paragraph(template,doc._body)
    pf=p.paragraph_format
    pf.left_indent=Inches(0); pf.right_indent=Inches(0); pf.first_line_indent=Inches(0)
    pf.space_before=Pt(before if before is not None else (10 if role=='sub' else 0))
    pf.space_after=Pt(after if after is not None else (12 if role in ['sub','chapter'] else 9))
    pf.line_spacing=1.15
    pf.keep_with_next=role in ['chapter','sub']
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER if center else (WD_ALIGN_PARAGRAPH.LEFT if role in ['chapter','sub','list'] else WD_ALIGN_PARAGRAPH.JUSTIFY)
    r=p.add_run(txt); r.font.name='Times New Roman'; r.font.size=Pt(size or (18 if role=='chapter' else 14 if role in ['sub','cover'] else 12)); r.bold=bold if bold is not None else role in ['chapter','sub','cover']
    return p
def chapter(t): return para(t,'chapter')
def sub(t): return para(t,'sub')
def page():
    p=para('',after=0); p.paragraph_format.line_spacing=1; p.add_run().add_break(__import__('docx').enum.text.WD_BREAK.PAGE)
def picture(name,width=6.6):
    p=para('',center=True,after=8); p.add_run().add_picture(str(TMP/name),width=Inches(width)); return p
def code(t):
    p=para(t,after=10); p.alignment=WD_ALIGN_PARAGRAPH.LEFT; p.paragraph_format.line_spacing=1
    for r in p.runs: r.font.name='Consolas'; r.font.size=Pt(10)
    return p
def tab(rows,widths):
    t=doc.add_table(rows=0,cols=len(rows[0])); t.autofit=False
    for c,w in zip(t.columns,widths): c.width=Inches(w)
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for c,w,txt in zip(cells,widths,row):
            c.width=Inches(w); p=c.paragraphs[0]; p.paragraph_format.space_after=Pt(6);p.paragraph_format.space_before=Pt(4)
            r=p.add_run(txt); r.font.name='Times New Roman';r.font.size=Pt(11);r.bold=ri==0
        if ri==0:
            e=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(e)
        for c in cells:
            tcPr=c._tc.get_or_add_tcPr(); borders=OxmlElement('w:tcBorders')
            for edge in ['top','left','bottom','right']:
                e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'777777');borders.append(e)
            tcPr.append(borders)
    return t

# 1 Cover, retaining the source college logo.
para('FOODBRIDGE', 'cover',True,after=4)
para('SURPLUS FOOD RESCUE PLATFORM','cover',True,after=24)
para('Integrated OOPS and DBMS project review','cover',True,after=22)
para('Submitted by',center=True,size=14,after=10)
for name in ['SANJAY P - 251501200','MOHAMMED SHAAHID AHMED - 251501136','BARATHKUMAR S - 251501030','NITISH S - 251501157']:
    para(name,'cover',True,after=8)
para('of',center=True,size=14,before=10,after=7)
para('BACHELOR OF ENGINEERING','cover',True,after=14)
para('in',center=True,size=14,after=7)
para('[DEPARTMENT NAME]','cover',True,after=22)
para('RAJALAKSHMI ENGINEERING COLLEGE, THANDALAM','cover',True,after=7)
para('(An Autonomous Institution)','cover',True,after=15)
picture('college-logo.png',3.8)
para('November 2026','cover',True,before=15,after=0)
page()
# 2 Certificate
para('RAJALAKSHMI ENGINEERING COLLEGE','cover',True,after=28)
para('BONAFIDE CERTIFICATE','cover',True,after=30)
para('Certified that this project report titled "FOODBRIDGE - SURPLUS FOOD RESCUE PLATFORM" is the bonafide work of SANJAY P (251501200), MOHAMMED SHAAHID AHMED (251501136), BARATHKUMAR S (251501030) and NITISH S (251501157), carried out under the supervision of the undersigned faculty members.',after=38)
t=doc.add_table(rows=1,cols=2)
for c,course in zip(t.rows[0].cells,['Object Oriented Programming','Database Management System']):
    for i,line in enumerate(['SIGNATURE','[FACULTY NAME]','Course Incharge',course,'[DEPARTMENT NAME]']):
        p=c.paragraphs[0] if i==0 else c.add_paragraph();p.paragraph_format.space_after=Pt(12)
        r=p.add_run(line);r.font.name='Times New Roman';r.font.size=Pt(12 if i>2 else 14);r.bold=i<3
para('INTERNAL EXAMINER                         EXTERNAL EXAMINER',bold=True,size=14,before=45)
page()
# 3 Abstract
para('ABSTRACT','cover',True,after=28)
for txt in [
'FoodBridge is a proposed surplus food rescue platform that connects restaurants, hotels, college canteens, event organizers and individuals with NGOs and volunteers. The project addresses the difficulty of locating available food, arranging collection within a short pickup window and maintaining a reliable record of each donation. Its goal is to reduce food waste and support access to food in line with Sustainable Development Goal 2, Zero Hunger, and Goal 12, Responsible Consumption and Production.',
'The platform is planned as a responsive website and an installable Progressive Web App. React, TypeScript and Tailwind CSS provide the frontend, while Java with Spring Boot handles business rules and access control. MySQL stores user accounts, organizations, food donations, claims, pickups, notifications and delivery records. Both web and mobile experiences use the same backend and database.',
'Java OOP concepts are applied through entity classes, private state, controlled methods, interfaces and service composition. A proposed user hierarchy demonstrates inheritance and polymorphism. SQL DBMS concepts are applied through related tables, primary and foreign keys, normalization, CRUD operations, joins, constraints, transactions and indexes. The donation claim operation connects both subjects: Java validates a request, and a database transaction protects the donation against duplicate claims.',
'The intended outcome is a useful food rescue application with role-specific dashboards, donation tracking and clearly defined impact estimates. This review presents the requirements, proposed design and validation approach for the project.'
]: para(txt,size=13,after=16)
page()
# 4 Contents
para('TABLE OF CONTENTS','cover',True,size=16,after=26)
toc=[('CHAPTER','CONTENTS','PAGE'),('1','INTRODUCTION','5'),('','Problem statement, overview, purpose and scope','5'),('2','FUNCTIONALITIES PROVIDED','6'),('3','SYSTEM FLOW DIAGRAM','7'),('','3.1 Dataflow diagram','8'),('','3.2 Use case diagram','9'),('','3.3 Entity relationship diagram','10'),('4','MODULE DESCRIPTION','11'),('','User modules and operational modules','11-12'),('5','IMPLEMENTATION','13'),('','5.1 Architecture and technology','13'),('','5.2 Java OOP design','14'),('','5.3 Illustrative Java design','15'),('','5.4 Database design and normalization','16'),('','5.5 SQL operations and reporting','17'),('','5.6 Transactions and validation','18'),('6','CONCLUSION','19'),('7','REFERENCES','20')]
toc_table=tab(toc,[1.0,5.2,.6])
for cell in [c for row in toc_table.rows for c in row.cells]:
    for edge in cell._tc.get_or_add_tcPr().find(qn('w:tcBorders')):
        edge.set(qn('w:val'),'nil')
page()
# 5 Introduction
chapter('1 - INTRODUCTION')
sub('1.1 PROBLEM STATEMENT')
para('Surplus edible food can remain unused when donors cannot quickly find a suitable recipient or arrange collection. Informal messages and phone calls provide limited visibility of quantity, pickup deadlines and delivery progress. A shared platform is needed to coordinate these steps and retain an accountable donation history.')
sub('1.2 PROJECT OVERVIEW')
para('FoodBridge connects donors, NGOs and volunteers through one rescue workflow. A donor publishes a donation with food details, quantity, photographs and pickup location. An NGO browses suitable donations and claims an available item. A volunteer accepts a pickup assignment and records progress until delivery. Administrators verify organizations and oversee platform activity.')
sub('1.3 PURPOSE')
para('The project aims to reduce food waste, support communities that need food and make rescue activity easier to coordinate. For the academic review, Java OOP and SQL DBMS form the working technical foundation: objects enforce behavior, while relational tables maintain reliable records.')
sub('1.4 SCOPE')
para('The initial scope covers registration, role-based access, donation posting, browsing, claiming, pickup coordination, notifications and impact reporting. A responsive website and installable PWA share a Java backend and MySQL database. Detailed citizen permissions and multi-role accounts require final decisions. An Android APK is a possible later extension.');page()
# 6 Features
chapter('2 - FUNCTIONALITIES PROVIDED')
sub('FUNCTIONALITIES PROVIDED BY FOODBRIDGE')
features=[('Registration and login','Users sign in with permissions appropriate to their role.'),('Donation posting','Donors add food type, quantity, unit, photos, pickup location and deadline.'),('Food discovery and matching','NGOs filter donations by location, availability and collection window.'),('Donation claims','Eligible NGOs claim available donations through a protected operation.'),('Volunteer coordination','Volunteers accept assignments and update pickup and delivery progress.'),('Food information and expiry','The platform displays handling details and blocks claims after the pickup deadline.'),('Dashboards and notifications','Each role sees relevant activity, history and pickup updates.'),('Administration','Administrators verify organizations and manage platform records.'),('Impact tracking','Reports count completed donations and present documented meal estimates.')]
for a,b in features: para(a+'. '+b,after=12)
para('Donor-supplied information and deadlines support coordination. They do not independently certify that food is safe to consume.',before=8);page()
# 7-10 diagrams
chapter('3 - SYSTEM FLOW DIAGRAM')
para('The system flow describes a successful donation journey. Each stage has a responsible user and a controlled status change. Cancellation and expiry provide alternate outcomes when rescue cannot continue.')
picture('flow.png',5.8)
para('Figure 3.1  Proposed FoodBridge donation workflow',center=True,size=11)
para('Suggested states: AVAILABLE, CLAIMED, ASSIGNED, PICKED_UP and DELIVERED. EXPIRED and CANCELLED represent alternate outcomes. A later stage must not occur before its required earlier stage.');page()
sub('3.1 DATAFLOW DIAGRAM')
para('This simplified dataflow diagram shows how donor details, claim requests and volunteer status updates reach persistent records. Processes validate requests before changing the related data store.')
picture('dfd.png')
para('Figure 3.2  Core donation, claim and delivery data flows',center=True,size=11)
para('The browser communicates with Java APIs. Backend services read or write MySQL through repositories. Supporting user and notification stores are omitted here to keep the main rescue flow readable.');page()
sub('3.2 USE CASE DIAGRAM')
para('The actors use FoodBridge for different tasks. Authentication applies to protected actions. Citizen functions shown below are limited to viewing community activity and impact until detailed permissions are finalized.')
picture('usecase.png')
para('Figure 3.3  Main actors and their proposed use cases',center=True,size=11)
para('Donors manage their own donations. NGOs manage their own claims. Volunteers update assigned pickups. Administrators handle verification and platform oversight.');page()
sub('3.3 ENTITY RELATIONSHIP DIAGRAM')
para('The core relational model connects the donor, donation, NGO claim and delivery journey. A foreign key references an existing parent record. The label 0..1 means that a related record is optional and unique.')
picture('erd.png')
para('Figure 3.4  Core FoodBridge entities and cardinalities',center=True,size=11)
para('This simplified model allows one claim record per donation and one pickup per claim. A future design for repeated claims after cancellation must explicitly separate active claims from claim history. Notifications and organization membership are supporting relationships described in the database section.');page()
# 11 Modules
chapter('4 - MODULE DESCRIPTION')
para('The modules group related user actions while keeping business rules in Java services.')
for head,txt in [
('4.1 HOME AND FOOD DISCOVERY','The home page explains the platform and guides users to explore or donate food. Explore Food displays available donations with location, quantity and pickup deadlines. Filters help recipients find suitable options.'),
('4.2 AUTHENTICATION AND PROFILE','Registration and login establish user identity. Spring Security is planned for authentication and authorization. Profile settings store contact information and preferences. Backend checks also verify ownership of each requested record.'),
('4.3 DONOR MODULE','The donor creates and updates donation details, supplies food information and tracks donation history. Once a claim exists, changes must follow explicit rules so that quantities and deadlines remain consistent with the agreement.'),
('4.4 NGO MODULE','NGO users browse donations, submit claim requests and follow pickup progress. Organization verification supports platform administration. A claim must identify the organization and the person who created it.')]: sub(head);para(txt)
page()
sub('4.5 VOLUNTEER AND PICKUP MODULE')
para('Volunteers view available assignments, accept a pickup and update collection progress. The platform records assignment, pickup and delivery timestamps. Delivery confirmation creates a record linked to the pickup rather than duplicating donation details.')
sub('4.6 NOTIFICATION MODULE')
para('Notifications communicate claim confirmations, assignment changes and delivery updates. NotificationSender defines a Java contract so that in-app and later email delivery can share a common calling interface. A success notification should follow a committed database change.')
sub('4.7 IMPACT CENTER')
para('The Impact Center summarizes completed donations and supported activity. Meal estimates require a documented conversion method and consistent units. Reports must avoid treating kilograms, servings and item counts as interchangeable values.')
sub('4.8 ADMINISTRATION MODULE')
para('Administrators review users and organizations, oversee donation activity and handle platform management. Important actions should leave an audit record. Permissions must limit access to personal information and prevent ordinary users from performing administrative operations.')
sub('4.9 CITIZEN DASHBOARD')
para('The citizen dashboard can present local community information and platform impact. Direct food claiming by citizens is not yet an agreed requirement. This permission must be defined before implementing the corresponding backend rules.');page()
# 13 Implementation
chapter('5 - IMPLEMENTATION')
sub('5.1 ARCHITECTURE AND TECHNOLOGY')
para('The proposed implementation uses separate presentation, application and persistence responsibilities. Both the website and the PWA call the same Java APIs. The following technology choices follow the project requirements.')
tab([('Layer','Technology and responsibility'),('Frontend','React and TypeScript for pages and user interaction'),('Styling','Tailwind CSS with cream, forest green, orange and white'),('Animation','Motion for React for restrained interface transitions'),('Application','Java and Spring Boot for APIs and business services'),('Access control','Spring Security for authentication and authorization'),('Persistence','Spring Data JPA over JDBC for relational data access'),('Database','MySQL for transactions, relationships and reports'),('Mobile delivery','PWA installation using the responsive web application')],[1.3,5.5])
sub('REQUEST PROCESSING')
para('A controller receives a request and validates its structure. A service checks business rules and coordinates the operation. A repository reads or writes database entities. The service returns a response that the frontend can display. Object-level authorization checks ensure that a user can act on the specific donation or pickup.')
para('Illustrative Java and SQL appear in the following sections. They explain the proposed design and do not represent verified application source code.');page()
# 14 OOP
sub('5.2 JAVA OOP DESIGN')
oop=[('Classes and objects','User, FoodDonation, DonationClaim, Pickup and Notification define model classes. A particular donation is an object with its own ID, quantity and deadline.'),('Encapsulation','Private fields protect donation state. A claim method checks availability and deadline before changing status, instead of exposing unrestricted status setters.'),('Inheritance and abstraction','A proposed abstract User contains shared identity. Donor, NgoUser and Volunteer extend it. NgoUser represents a person, while Organization represents the institution.'),('Polymorphism','Each user subtype can override dashboardSummary(). A User reference invokes the appropriate implementation at runtime.'),('Interfaces','NotificationSender defines a send operation. InAppNotificationSender and a future EmailNotificationSender implement that contract.'),('Composition','DonationService has a repository and a notification sender. Pickup refers to its claim and assigned volunteer. These objects cooperate through explicit dependencies.'),('Exception handling','DonationUnavailableException reports an expired or already claimed donation. A controller maps it to a clear error, and failed database work rolls back.')]
for a,b in oop: para(a+'. '+b,after=13)
para('The proposed inheritance example assumes one primary role per account. If accounts need multiple roles, a UserRoles relation and composed capabilities offer a more flexible model.');page()
# 15 Java
sub('5.3 ILLUSTRATIVE JAVA DESIGN')
para('The example below demonstrates abstraction, inheritance and runtime polymorphism. A class defines the contract, and each subtype supplies its own dashboard description.')
code('abstract class User {\n    private final long id;\n    protected User(long id) { this.id = id; }\n    public long getId() { return id; }\n    public abstract String dashboardSummary();\n}\n\nfinal class Donor extends User {\n    Donor(long id) { super(id); }\n    @Override\n    public String dashboardSummary() {\n        return "My donations and pickup status";\n    }\n}\n\nfinal class Volunteer extends User {\n    Volunteer(long id) { super(id); }\n    @Override\n    public String dashboardSummary() {\n        return "My assigned pickups";\n    }\n}')
sub('INTERFACE AND COMPOSITION EXAMPLE')
code('interface NotificationSender {\n    void send(long recipientId, String message);\n}\n\nfinal class DonationService {\n    private final NotificationSender sender;\n    DonationService(NotificationSender sender) {\n        this.sender = sender;\n    }\n}')
para('The service depends on a notification contract. Different implementations can handle the same call. Actual claim processing also needs repositories, authorization and a transaction.');page()
# 16 database
sub('5.4 DATABASE DESIGN AND NORMALIZATION')
tab([('Table','Key fields and purpose'),('Users','user_id PK; unique email; password_hash; primary_role'),('Organizations','organization_id PK; name; verification_status'),('OrganizationMembers','user_id + organization_id composite PK and FKs'),('FoodDonations','donation_id PK; donor_id FK; quantity; unit; status; deadline'),('DonationClaims','claim_id PK; donation_id UNIQUE FK; organization_id FK'),('Pickups','pickup_id PK; claim_id UNIQUE FK; volunteer_id FK'),('DeliveryRecords','delivery_id PK; pickup_id UNIQUE FK; delivered_at'),('Notifications','notification_id PK; recipient_user_id FK; message; read_at')],[1.9,4.9])
sub('NORMALIZATION')
para('First normal form keeps one value per field. Multiple photographs belong in DonationPhotos rows. Second normal form requires attributes of OrganizationMembers to depend on the complete user-and-organization key. Third normal form stores organization details in Organizations instead of repeating them in each claim.')
sub('CONSTRAINTS AND INDEXES')
para('Primary keys identify records, foreign keys protect references, and NOT NULL marks required values. Unique email prevents duplicate accounts. A quantity check rejects non-positive values. A candidate index on status and pickup_deadline supports availability queries. EXPLAIN and realistic data help confirm whether that index is useful.');page()
# 17 SQL
sub('5.5 SQL OPERATIONS AND REPORTING')
para('These illustrative statements demonstrate CRUD operations and a join using the proposed schema. Question marks represent values bound by a prepared statement.')
code("-- CREATE a donation\nINSERT INTO FoodDonations\n  (donor_id, food_name, quantity, unit, status, pickup_deadline)\nVALUES (?, ?, ?, ?, 'AVAILABLE', ?);\n\n-- READ available donations\nSELECT donation_id, food_name, quantity, unit\nFROM FoodDonations\nWHERE status = 'AVAILABLE'\n  AND pickup_deadline > CURRENT_TIMESTAMP\nORDER BY pickup_deadline;\n\n-- UPDATE an unclaimed donation owned by the caller\nUPDATE FoodDonations SET food_name = ?\nWHERE donation_id = ? AND donor_id = ?\n  AND status = 'AVAILABLE';\n\n-- DELETE an old notification owned by the caller\nDELETE FROM Notifications\nWHERE notification_id = ? AND recipient_user_id = ?;")
sub('JOIN AND AGGREGATE REPORT')
code("SELECT u.user_id, u.name, COUNT(*) AS completed_donations\nFROM Users u\nJOIN FoodDonations d ON d.donor_id = u.user_id\nWHERE d.status = 'DELIVERED'\nGROUP BY u.user_id, u.name;")
para('This report returns completed donation counts for donors with at least one delivery. The application binds the authenticated user ID rather than trusting a caller-supplied identity. Cancellation preserves donation history more safely than deleting records with claims.');page()
# 18 Transactions / validation
sub('5.6 TRANSACTIONS AND VALIDATION')
para('Two NGOs may try to claim the same donation. The claim service must validate authorization and coordinate the update and insertion inside one transaction. The following pseudocode describes the database steps.')
code("BEGIN;\nUPDATE FoodDonations SET status = 'CLAIMED'\nWHERE donation_id = ? AND status = 'AVAILABLE'\n  AND pickup_deadline > CURRENT_TIMESTAMP;\n-- Proceed only if exactly one row changed\nINSERT INTO DonationClaims\n  (donation_id, organization_id, claimed_by_user_id)\nVALUES (?, ?, ?);\nCOMMIT;\n-- Roll back if validation or insertion fails")
para('With MySQL InnoDB, the conditional update coordinates competing requests. A unique donation_id in DonationClaims adds a second safeguard for the simplified one-claim model. Spring transaction management can commit both steps together or roll them back on failure.')
para('Atomicity keeps the steps together. Consistency preserves constraints. Isolation controls concurrent work. Durability preserves a committed result. Notifications should reflect committed changes.')
sub('PLANNED VALIDATION CASES')
tab([('Scenario','Expected behavior'),('Valid donation','Store required details and show availability'),('Expired donation','Reject the claim without inserting a record'),('Two simultaneous claims','Allow one claim; return a conflict for the other'),('Unauthorized update','Reject the operation and preserve the record'),('Failure during claim save','Roll back the donation status change'),('Confirmed delivery','Record receipt and update completed donation counts')],[2.2,4.6])
page()
# 19 Conclusion
chapter('6 - CONCLUSION')
para('FoodBridge proposes a coordinated way to rescue surplus edible food through donors, NGOs and volunteers. Its central workflow covers posting, claiming, collection and delivery, with role-specific dashboards and a traceable donation history. The project connects a practical community need with the academic requirements of Java OOP and SQL DBMS.')
para('The object model gives responsibilities to classes and services. Encapsulation protects state, inheritance and abstraction support shared behavior, polymorphism enables role-specific behavior, and interfaces allow interchangeable notification implementations. Composition connects these objects without placing every responsibility in one class.')
para('The relational design maintains connected records through primary and foreign keys. Normalization reduces duplication. Constraints and transactions protect the claim workflow, while joins and aggregate queries support reporting. These database features must work alongside Java validation rather than remain documentation-only concepts.')
sub('EXPECTED OUTCOME')
para('The intended result is a responsive website and an installable PWA backed by Java and MySQL. A successful demonstration should complete a donation journey, reject invalid actions and show the underlying SQL relationships and transaction behavior. The planned validation cases provide the basis for recording results during implementation.')
sub('FUTURE ENHANCEMENTS')
para('Later extensions may include improved distance matching, delivery route assistance, additional notification channels and an Android APK. Any expansion should preserve access control, donation history and a documented method for estimating impact.');page()
# 20 References
chapter('7 - REFERENCES')
refs=[('1. FoodBridge project requirements','Team-provided scope, role descriptions, technology choices and academic requirements.'),('2. Oracle Java Tutorials','Object-Oriented Programming Concepts. Classes, objects, inheritance and interfaces.\nhttps://docs.oracle.com/javase/tutorial/java/concepts/'),('3. Spring Data JPA Reference','Repository support and relational persistence using JPA.\nhttps://docs.spring.io/spring-data/jpa/reference/'),('4. Spring Security Reference','Authentication and authorization for Spring applications.\nhttps://docs.spring.io/spring-security/reference/')]
refs.append(('5. MySQL Reference Manual','InnoDB and the ACID Model. Transaction guarantees and relational storage.\nhttps://dev.mysql.com/doc/refman/8.4/en/mysql-acid.html'))
for a,b in refs:
    sub(a)
    para(b,after=20).alignment=WD_ALIGN_PARAGRAPH.LEFT
para('Documentation accessed on 4 November 2026. The Oracle tutorial explains foundational OOP concepts and identifies JDK 8 as its baseline. Project dependency versions should be selected and documented during implementation.',size=11,before=16)

# Source section page geometry and footer assets remain in use.
doc.core_properties.title='FoodBridge Surplus Food Rescue Platform Project Review'
doc.core_properties.author='Sanjay P; Mohammed Shaahid Ahmed; BarathKumar S; Nitish S'
doc.core_properties.subject='Integrated OOPS and DBMS project review'
doc.core_properties.comments=''
settings=doc.settings.element
uf=settings.find(qn('w:updateFields'))
if uf is None: uf=OxmlElement('w:updateFields');settings.append(uf)
uf.set(qn('w:val'),'true')
interim=TMP/'authored.docx';doc.save(interim)
# Preserve all unchanged opaque package parts exactly from the retained template.
editable={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml','word/settings.xml','docProps/core.xml'}
with ZipFile(REF) as src, ZipFile(interim) as new, ZipFile(OUT,'w',ZIP_DEFLATED) as dst:
    added=set(new.namelist())-set(src.namelist())
    for name in src.namelist(): dst.writestr(name,new.read(name) if name in editable else src.read(name))
    for name in added: dst.writestr(name,new.read(name))
with ZipFile(REF) as src, ZipFile(OUT) as final:
    changed=[n for n in src.namelist() if src.read(n)!=final.read(n)]
    assert set(changed)<=editable,changed
assert sha256(REF.read_bytes()).hexdigest()==digest
(TMP/'fidelity.json').write_text(json.dumps({'reference_sha256':digest,'changed_source_parts':changed,'added_parts':sorted(added),'intended_pages':20},indent=2))
print(str(OUT))
