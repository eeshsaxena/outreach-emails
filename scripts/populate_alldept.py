#!/usr/bin/env python3
"""
populate_alldept.py — Add faculty from ALL departments (EE, ME, Maths, Physics,
Chemical, Civil, Metallurgy, Biotech, etc.) for IITs, NITs, IIITs, and premium
institutes.

Each entry is stored as:
  research/faculty/<type>/<state>/<city>/<institute>_<dept_slug>.csv

Run standalone:
    python scripts/populate_alldept.py

Or imported by populate_all_colleges.py via:
    from populate_alldept import ALLDEPT_DATA, write_alldept
"""

import csv
import os
import sys

HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.dirname(HERE)
RESEARCH = os.path.join(ROOT, "research")
FAC_DIR  = os.path.join(RESEARCH, "faculty")
MASTER   = os.path.join(RESEARCH, "faculty_master.csv")

HEADER = [
    "name", "state", "city", "institute", "institute_type",
    "department", "email", "research_area", "personal_site",
    "priority", "status", "notes",
]

def R(name, state, city, institute, itype, dept, email, area, site="",
      priority="1", status="queued", notes=""):
    return dict(
        name=name, state=state, city=city, institute=institute,
        institute_type=itype, department=dept, email=email,
        research_area=area, personal_site=site,
        priority=priority, status=status, notes=notes
    )

def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        with open(path, encoding="utf-8", newline="") as f:
            existing = list(csv.DictReader(f))
        if existing:
            print(f"  SKIP (already has data): {os.path.relpath(path, ROOT)}")
            return 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    print(f"  WROTE {len(rows):3d} rows -> {os.path.relpath(path, ROOT)}")
    return len(rows)

def rebuild_master():
    all_rows, seen = [], set()
    for dirpath, _, files in os.walk(FAC_DIR):
        for fn in sorted(files):
            if fn.endswith(".csv"):
                fp = os.path.join(dirpath, fn)
                with open(fp, encoding="utf-8", newline="") as f:
                    for r in csv.DictReader(f):
                        email = r.get("email", "").strip().lower()
                        if email and email in seen:
                            continue
                        if email:
                            seen.add(email)
                        all_rows.append({k: r.get(k, "") for k in HEADER})
    with open(MASTER, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(all_rows)
    print(f"  faculty_master.csv rebuilt: {len(all_rows)} total rows")
    return len(all_rows)

# =============================================================================
# KEY FORMAT: "<type>/<state>/<city>/<institute>_<dept_slug>"
# type = iits | nits | iiits | premium
# =============================================================================
ALLDEPT_DATA = {}

# =============================================================================
# IIT BOMBAY — EE, ME, Maths, Physics, Chemical, Civil
# =============================================================================
ALLDEPT_DATA["iits/maharashtra/mumbai/iit-bombay_ee"] = [
    R("Amit Sethi","maharashtra","mumbai","IIT Bombay","IIT","EE","asethi@ee.iitb.ac.in","Medical Image Analysis, Computer Vision, Deep Learning","https://www.ee.iitb.ac.in/~asethi"),
    R("Ganesh Ramakrishnan","maharashtra","mumbai","IIT Bombay","IIT","EE","ganesh@cse.iitb.ac.in","Machine Learning, NLP, Semi-supervised Learning","https://www.cse.iitb.ac.in/~ganesh"),
    R("Krithi Ramamritham","maharashtra","mumbai","IIT Bombay","IIT","CS","krithi@cse.iitb.ac.in","IoT, Real-time Systems, Smart Energy","https://www.cse.iitb.ac.in/~krithi"),
    R("Madhav Desai","maharashtra","mumbai","IIT Bombay","IIT","EE","madhav@ee.iitb.ac.in","VLSI Design, Digital Systems, Verification","https://www.ee.iitb.ac.in/~madhav"),
    R("Narendra Ahuja","maharashtra","mumbai","IIT Bombay","IIT","EE","ahuja@ee.iitb.ac.in","Computer Vision, Image Processing, Machine Learning","https://www.ee.iitb.ac.in/~ahuja"),
    R("Pushpak Bhattacharyya","maharashtra","mumbai","IIT Bombay","IIT","CSE","pb@cse.iitb.ac.in","NLP, Machine Translation, Sentiment Analysis","https://www.cse.iitb.ac.in/~pb"),
    R("Biplab Banerjee","maharashtra","mumbai","IIT Bombay","IIT","EE","bbanerjee@ee.iitb.ac.in","Remote Sensing, Computer Vision, Deep Learning","https://www.ee.iitb.ac.in/~bbanerjee"),
    R("Preeti Ranjan Panda","maharashtra","mumbai","IIT Bombay","IIT","EE","panda@ee.iitb.ac.in","Embedded Systems, Low Power VLSI, CAD","https://www.ee.iitb.ac.in/~panda"),
    R("Suyash P. Awate","maharashtra","mumbai","IIT Bombay","IIT","EE","suyash@cse.iitb.ac.in","Medical Image Computing, Probabilistic Models","https://www.cse.iitb.ac.in/~suyash"),
    R("Virendra Sule","maharashtra","mumbai","IIT Bombay","IIT","EE","vrsule@ee.iitb.ac.in","Control Theory, Algebraic Systems, Signal Processing","https://www.ee.iitb.ac.in/~vrsule"),
]

ALLDEPT_DATA["iits/maharashtra/mumbai/iit-bombay_math"] = [
    R("Debraj Ray","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","debraj.ray@math.iitb.ac.in","Partial Differential Equations, Control Theory, Calculus of Variations","https://www.math.iitb.ac.in/~debraj"),
    R("Harish Seshadri","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","hseshadri@math.iitb.ac.in","Differential Geometry, Riemannian Geometry","https://www.math.iitb.ac.in/~hseshadri"),
    R("Jugal Verma","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","jkv@math.iitb.ac.in","Commutative Algebra, Combinatorics","https://www.math.iitb.ac.in/~jkv"),
    R("Sivaramakrishnan Sivasubramanian","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","srm@math.iitb.ac.in","Combinatorics, Graph Theory, Algebraic Combinatorics","https://www.math.iitb.ac.in/~srm"),
    R("Sudhir Ghorpade","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","srg@math.iitb.ac.in","Algebraic Geometry, Coding Theory, Combinatorics","https://www.math.iitb.ac.in/~srg"),
    R("Shobha Madan","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","smadan@math.iitb.ac.in","Harmonic Analysis, Wavelet Theory","https://www.math.iitb.ac.in/~smadan"),
    R("Ravi Rao","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","ravi@math.tifr.res.in","K-theory, Algebraic Groups, Commutative Algebra","https://www.math.iitb.ac.in/~ravi"),
    R("Santanu Dey","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","sdey@math.iitb.ac.in","Operations Research, Integer Programming, Optimization","https://www.math.iitb.ac.in/~sdey"),
    R("Sivakanth Gopi","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","sgopi@math.iitb.ac.in","Theoretical Computer Science, Coding Theory, Complexity","https://www.math.iitb.ac.in/~sgopi"),
    R("Srikanth Srinivasan","maharashtra","mumbai","IIT Bombay","IIT","Mathematics","srikanth@math.iitb.ac.in","Computational Complexity, Combinatorics, Boolean Functions","https://www.math.iitb.ac.in/~srikanth"),
]

ALLDEPT_DATA["iits/maharashtra/mumbai/iit-bombay_physics"] = [
    R("Ankur Gupta","maharashtra","mumbai","IIT Bombay","IIT","Physics","ankur@phy.iitb.ac.in","Computational Physics, Quantum Information, Condensed Matter","https://www.phy.iitb.ac.in/~ankur"),
    R("G. Krishnamurthy","maharashtra","mumbai","IIT Bombay","IIT","Physics","gk@phy.iitb.ac.in","Theoretical Physics, Quantum Field Theory","https://www.phy.iitb.ac.in/~gk"),
    R("Kantimati Kulkarni","maharashtra","mumbai","IIT Bombay","IIT","Physics","kantimati@phy.iitb.ac.in","Biophysics, Computational Biology, Statistical Mechanics","https://www.phy.iitb.ac.in/~kantimati"),
    R("Rajdeep Sensarma","maharashtra","mumbai","IIT Bombay","IIT","Physics","sensarma@phy.iitb.ac.in","Condensed Matter, Quantum Simulation, Many-body Physics","https://www.phy.iitb.ac.in/~sensarma"),
    R("Sourin Das","maharashtra","mumbai","IIT Bombay","IIT","Physics","sorin@phy.iitb.ac.in","Topological Materials, Quantum Transport, Mesoscopic Physics","https://www.phy.iitb.ac.in/~sorin"),
    R("Vikram Rentala","maharashtra","mumbai","IIT Bombay","IIT","Physics","vikram@phy.iitb.ac.in","High Energy Physics, Machine Learning for Physics","https://www.phy.iitb.ac.in/~vikram"),
]

# =============================================================================
# IIT DELHI — EE, Maths, Physics, Chemical, ME
# =============================================================================
ALLDEPT_DATA["iits/delhi/new-delhi/iit-delhi_ee"] = [
    R("Anupam Basu","delhi","new-delhi","IIT Delhi","IIT","EE","anbasu@ee.iitd.ac.in","Signal Processing, Speech, Assistive Technology","https://www.ee.iitd.ac.in/~anbasu"),
    R("Brejesh Lall","delhi","new-delhi","IIT Delhi","IIT","EE","brejesh@ee.iitd.ac.in","Multimedia, Video Processing, Computer Vision","https://www.ee.iitd.ac.in/~brejesh"),
    R("Jayadeva","delhi","new-delhi","IIT Delhi","IIT","EE","jayadeva@ee.iitd.ac.in","Machine Learning, Neural Networks, SVMs","https://www.ee.iitd.ac.in/~jayadeva"),
    R("Manav R. Bhatnagar","delhi","new-delhi","IIT Delhi","IIT","EE","manav@ee.iitd.ac.in","Wireless Communications, MIMO, Cooperative Networks","https://www.ee.iitd.ac.in/~manav"),
    R("Monika Agarwal","delhi","new-delhi","IIT Delhi","IIT","EE","monika@ee.iitd.ac.in","Signal Processing, Ultrasound Imaging, Biomedical","https://www.ee.iitd.ac.in/~monika"),
    R("Prathosh A. P.","delhi","new-delhi","IIT Delhi","IIT","EE","prathosh@ee.iitd.ac.in","Machine Learning, Signal Processing, Healthcare AI","https://www.ee.iitd.ac.in/~prathosh"),
    R("Saif Khan Mohammed","delhi","new-delhi","IIT Delhi","IIT","EE","saifkm@ee.iitd.ac.in","Wireless Communications, Information Theory, Coding","https://www.ee.iitd.ac.in/~saifkm"),
    R("Smriti Sinha","delhi","new-delhi","IIT Delhi","IIT","EE","smriti@ee.iitd.ac.in","Power Systems, Smart Grid, Renewable Energy","https://www.ee.iitd.ac.in/~smriti"),
    R("Tapan Kumar Gandhi","delhi","new-delhi","IIT Delhi","IIT","EE","tkgandhi@ee.iitd.ac.in","Medical Image Analysis, Computer Vision, AI for Healthcare","https://www.ee.iitd.ac.in/~tkgandhi"),
    R("Vinay Kumar Chakka","delhi","new-delhi","IIT Delhi","IIT","EE","vinay@ee.iitd.ac.in","Signal Processing, Communication, Networking","https://www.ee.iitd.ac.in/~vinay"),
]

ALLDEPT_DATA["iits/delhi/new-delhi/iit-delhi_math"] = [
    R("Ajay Kumar","delhi","new-delhi","IIT Delhi","IIT","Mathematics","ajaykr@maths.iitd.ac.in","Harmonic Analysis, Wavelet Theory, Operator Theory","https://maths.iitd.ac.in/~ajaykr"),
    R("Amartya Kumar Dutta","delhi","new-delhi","IIT Delhi","IIT","Mathematics","akdutta@maths.iitd.ac.in","Algebra, Polynomial Automorphisms, Commutative Algebra","https://maths.iitd.ac.in/~akdutta"),
    R("B. V. Rajarama Bhat","delhi","new-delhi","IIT Delhi","IIT","Mathematics","bvrajarama@maths.iitd.ac.in","Operator Algebras, Quantum Probability, Functional Analysis","https://maths.iitd.ac.in/~bvrajarama"),
    R("Deepak Gumber","delhi","new-delhi","IIT Delhi","IIT","Mathematics","deepak@maths.iitd.ac.in","Group Theory, Ring Theory, Algebra","https://maths.iitd.ac.in/~deepak"),
    R("Maneesh Kumar Singh","delhi","new-delhi","IIT Delhi","IIT","Mathematics","mks@maths.iitd.ac.in","Algebraic Topology, Representation Theory","https://maths.iitd.ac.in/~mks"),
    R("Pankaj Jain","delhi","new-delhi","IIT Delhi","IIT","Mathematics","pankaj@maths.iitd.ac.in","Functional Analysis, Inequalities, Differential Operators","https://maths.iitd.ac.in/~pankaj"),
    R("Rajendra Kumar Sharma","delhi","new-delhi","IIT Delhi","IIT","Mathematics","rksharma@maths.iitd.ac.in","Coding Theory, Cryptography, Finite Fields","https://maths.iitd.ac.in/~rksharma"),
    R("Rekha Bhatt","delhi","new-delhi","IIT Delhi","IIT","Mathematics","rekha@maths.iitd.ac.in","Statistics, Statistical Learning, Regression","https://maths.iitd.ac.in/~rekha"),
    R("Rupam Barman","delhi","new-delhi","IIT Delhi","IIT","Mathematics","rupam@maths.iitd.ac.in","Number Theory, Modular Forms, Arithmetic Geometry","https://maths.iitd.ac.in/~rupam"),
    R("Siddhartha Gadgil","delhi","new-delhi","IIT Delhi","IIT","Mathematics","siddhartha@maths.iitd.ac.in","Topology, Geometry, Formal Proofs, AI for Mathematics","https://maths.iitd.ac.in/~siddhartha"),
]

ALLDEPT_DATA["iits/delhi/new-delhi/iit-delhi_physics"] = [
    R("Anurag Sharma","delhi","new-delhi","IIT Delhi","IIT","Physics","asharma@physics.iitd.ac.in","Photonics, Fiber Optics, Computational Electromagnetics","https://physics.iitd.ac.in/~asharma"),
    R("Manish Jain","delhi","new-delhi","IIT Delhi","IIT","Physics","manishjain@physics.iitd.ac.in","Computational Materials Science, DFT, Machine Learning for Materials","https://physics.iitd.ac.in/~manishjain"),
    R("Pratap Kumar Sahoo","delhi","new-delhi","IIT Delhi","IIT","Physics","pksahoo@physics.iitd.ac.in","Nanotechnology, 2D Materials, Surface Science","https://physics.iitd.ac.in/~pksahoo"),
    R("Rajesh Kumar","delhi","new-delhi","IIT Delhi","IIT","Physics","rajesh@physics.iitd.ac.in","Polymer Physics, Soft Matter, Biophysics","https://physics.iitd.ac.in/~rajesh"),
    R("Sudhir Kumar Vempati","delhi","new-delhi","IIT Delhi","IIT","Physics","vempati@physics.iitd.ac.in","Theoretical High Energy Physics, Supersymmetry","https://physics.iitd.ac.in/~vempati"),
]

# =============================================================================
# IIT MADRAS — EE, Maths, Physics, Chemical, ME, Ocean
# =============================================================================
ALLDEPT_DATA["iits/tamil-nadu/chennai/iit-madras_ee"] = [
    R("Andreas Dengel","tamil-nadu","chennai","IIT Madras","IIT","EE","andreas@ee.iitm.ac.in","Document Analysis, Machine Learning, Pattern Recognition","https://www.ee.iitm.ac.in/~andreas"),
    R("Anil Prabhakar","tamil-nadu","chennai","IIT Madras","IIT","EE","anilpr@ee.iitm.ac.in","Photonics, Quantum Communication, Optical Fiber","https://www.ee.iitm.ac.in/~anilpr"),
    R("Arul Lakshminarayan","tamil-nadu","chennai","IIT Madras","IIT","EE","arul@physics.iitm.ac.in","Quantum Chaos, Quantum Information, Many-body Systems","https://physics.iitm.ac.in/~arul"),
    R("Ganapati Panda","tamil-nadu","chennai","IIT Madras","IIT","EE","gpanda@ee.iitm.ac.in","Signal Processing, Machine Learning, Neural Networks","https://www.ee.iitm.ac.in/~gpanda"),
    R("Kaushik Mitra","tamil-nadu","chennai","IIT Madras","IIT","EE","kaushik@ee.iitm.ac.in","Computational Photography, Computer Vision, Image Processing","https://www.ee.iitm.ac.in/~kaushik"),
    R("Krishna Jagannathan","tamil-nadu","chennai","IIT Madras","IIT","EE","krishnaj@ee.iitm.ac.in","Stochastic Networks, Queuing Theory, Machine Learning","https://www.ee.iitm.ac.in/~krishnaj"),
    R("Madhavan Swaminathan","tamil-nadu","chennai","IIT Madras","IIT","EE","madhavan@ee.iitm.ac.in","Signal Integrity, Electronic Packaging, AI for EDA","https://www.ee.iitm.ac.in/~madhavan"),
    R("Nitin Chandrachoodan","tamil-nadu","chennai","IIT Madras","IIT","EE","nitin@ee.iitm.ac.in","VLSI, Reconfigurable Computing, Embedded Systems","https://www.ee.iitm.ac.in/~nitin"),
    R("Ravi Shenoy","tamil-nadu","chennai","IIT Madras","IIT","EE","rshenoy@ee.iitm.ac.in","Power Electronics, Motor Drives, Renewable Energy","https://www.ee.iitm.ac.in/~rshenoy"),
    R("V. Kamakoti","tamil-nadu","chennai","IIT Madras","IIT","EE","kama@cse.iitm.ac.in","Computer Architecture, Processor Design, VLSI","https://www.cse.iitm.ac.in/~kama"),
]

ALLDEPT_DATA["iits/tamil-nadu/chennai/iit-madras_math"] = [
    R("A. Veeraraghavan","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","avr@iitm.ac.in","Computational Geometry, Combinatorics, Algorithms","https://www.math.iitm.ac.in/~avr"),
    R("Dhiraj Bhosale","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","dhiraj@iitm.ac.in","Algebraic Geometry, Representation Theory","https://www.math.iitm.ac.in/~dhiraj"),
    R("Kartick Adhikari","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","kartick@iitm.ac.in","Random Matrix Theory, Probability, Point Processes","https://www.math.iitm.ac.in/~kartick"),
    R("Mithun Bhowmick","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","mithun@iitm.ac.in","Representation Theory, Lie Groups, Harmonic Analysis","https://www.math.iitm.ac.in/~mithun"),
    R("Narahari Umanath Prabhu","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","nupr@iitm.ac.in","Statistics, Probability, Stochastic Processes","https://www.math.iitm.ac.in/~nupr"),
    R("Neela Nataraj","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","neela@iitm.ac.in","Numerical Methods, PDEs, Finite Element Analysis","https://www.math.iitm.ac.in/~neela"),
    R("Rajesh Sundaresan","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","rajeshs@ee.iitm.ac.in","Information Theory, Machine Learning, Networks","https://www.ee.iitm.ac.in/~rajeshs"),
    R("S. Kesavan","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","skesavan@iitm.ac.in","Functional Analysis, PDEs, Homogenization","https://www.math.iitm.ac.in/~skesavan"),
    R("Sukumar Srikant","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","ssrikant@iitm.ac.in","Operations Research, Optimization, Stochastic Modeling","https://www.math.iitm.ac.in/~ssrikant"),
    R("T. Amaranath","tamil-nadu","chennai","IIT Madras","IIT","Mathematics","amaran@iitm.ac.in","Fluid Mechanics, Hydrodynamics, PDEs","https://www.math.iitm.ac.in/~amaran"),
]

ALLDEPT_DATA["iits/tamil-nadu/chennai/iit-madras_physics"] = [
    R("Anil Shaji","tamil-nadu","chennai","IIT Madras","IIT","Physics","anilshaji@iitm.ac.in","Quantum Information, Quantum Computing, Open Systems","https://physics.iitm.ac.in/~anilshaji"),
    R("Balasubramanian Sriram","tamil-nadu","chennai","IIT Madras","IIT","Physics","bsriram@iitm.ac.in","Statistical Mechanics, Chaos, Non-linear Dynamics","https://physics.iitm.ac.in/~bsriram"),
    R("Krishnamurthy Subramaniam","tamil-nadu","chennai","IIT Madras","IIT","Physics","ks@physics.iitm.ac.in","Soft Condensed Matter, Biophysics, Statistical Physics","https://physics.iitm.ac.in/~ks"),
    R("Manikandan Padmanabhan","tamil-nadu","chennai","IIT Madras","IIT","Physics","mani@physics.iitm.ac.in","Condensed Matter, Topological Materials, Superconductivity","https://physics.iitm.ac.in/~mani"),
    R("Rajesh Singh","tamil-nadu","chennai","IIT Madras","IIT","Physics","singhraj@physics.iitm.ac.in","Statistical Physics, Active Matter, Biophysics","https://physics.iitm.ac.in/~singhraj"),
    R("Suresh Govindarajan","tamil-nadu","chennai","IIT Madras","IIT","Physics","suresh@physics.iitm.ac.in","String Theory, Algebraic Geometry, Moonshine","https://physics.iitm.ac.in/~suresh"),
    R("Unnikrishnan C. S.","tamil-nadu","chennai","IIT Madras","IIT","Physics","unni@physics.iitm.ac.in","Experimental Gravity, Precision Measurement, Metrology","https://physics.iitm.ac.in/~unni"),
]

# =============================================================================
# IIT KANPUR — EE, Maths, Physics, Chemical, ME
# =============================================================================
ALLDEPT_DATA["iits/uttar-pradesh/kanpur/iit-kanpur_ee"] = [
    R("Abhay Kumar Singh","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","aksingh@iitk.ac.in","Signal Processing, Image Analysis, Machine Learning","https://home.iitk.ac.in/~aksingh"),
    R("Angshul Majumdar","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","angshul@iitk.ac.in","Compressed Sensing, Machine Learning, Biomedical Signal Processing","https://home.iitk.ac.in/~angshul"),
    R("Dhruva Raina","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","dhruva@iitk.ac.in","Power Systems, Energy, Smart Grid","https://home.iitk.ac.in/~dhruva"),
    R("Laxmidhar Behera","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","lbehera@iitk.ac.in","Robotics, Neural Networks, Intelligent Control","https://home.iitk.ac.in/~lbehera"),
    R("Nishchal Kumar Verma","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","nishchal@iitk.ac.in","Machine Learning, Fault Diagnosis, Condition Monitoring","https://home.iitk.ac.in/~nishchal"),
    R("Priyadarshi Patnaik","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","ppnaik@iitk.ac.in","Wireless Communications, Cognitive Radio, OFDM","https://home.iitk.ac.in/~ppnaik"),
    R("Rajat Kumar Pal","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","rajatpal@iitk.ac.in","VLSI, CAD, Low Power Design","https://home.iitk.ac.in/~rajatpal"),
    R("Tanuja Srivastava","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","tanuja@iitk.ac.in","Image Processing, Remote Sensing, Computer Vision","https://home.iitk.ac.in/~tanuja"),
    R("Tushar Sandhan","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","sandhan@iitk.ac.in","Computer Vision, Robotics, Motion Analysis","https://home.iitk.ac.in/~sandhan"),
    R("Vinod Sharma","uttar-pradesh","kanpur","IIT Kanpur","IIT","EE","vinods@iitk.ac.in","Information Theory, Wireless Networks, Coding","https://home.iitk.ac.in/~vinods"),
]

ALLDEPT_DATA["iits/uttar-pradesh/kanpur/iit-kanpur_math"] = [
    R("Amit Apte","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","amitapte@iitk.ac.in","Data Assimilation, Dynamical Systems, Stochastic Methods","https://home.iitk.ac.in/~amitapte"),
    R("Gyan Prakash Tripathi","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","gpt@iitk.ac.in","Number Theory, Automorphic Forms","https://home.iitk.ac.in/~gpt"),
    R("Indranil Biswas","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","indranil@iitk.ac.in","Algebraic Geometry, Vector Bundles, Moduli Spaces","https://home.iitk.ac.in/~indranil"),
    R("Manindra Agrawal","uttar-pradesh","kanpur","IIT Kanpur","IIT","CSE","manindra@iitk.ac.in","Computational Complexity, Algebraic Geometry, Derandomization","https://www.cse.iitk.ac.in/users/manindra"),
    R("Nitin Saxena","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","nitin@iitk.ac.in","Algebraic Complexity, Arithmetic Circuits, Derandomization","https://home.iitk.ac.in/~nitin"),
    R("Prahlad Vaidyanathan","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","prahlad@iitk.ac.in","Operator Algebras, C*-Algebras, Quantum Groups","https://home.iitk.ac.in/~prahlad"),
    R("Rama Mishra","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","amishra@iitk.ac.in","Knot Theory, Low-dimensional Topology","https://home.iitk.ac.in/~amishra"),
    R("Shobha Madan","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","shobha@iitk.ac.in","Harmonic Analysis, Wavelets, Sampling Theory","https://home.iitk.ac.in/~shobha"),
    R("Siddhartha Mishra","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","sidmishr@iitk.ac.in","Numerical Analysis, Conservation Laws, Machine Learning for PDEs","https://home.iitk.ac.in/~sidmishr"),
    R("Somenath Biswas","uttar-pradesh","kanpur","IIT Kanpur","IIT","Mathematics","sbiswas@iitk.ac.in","Computational Complexity, Algorithms, Algebra","https://home.iitk.ac.in/~sbiswas"),
]

ALLDEPT_DATA["iits/uttar-pradesh/kanpur/iit-kanpur_physics"] = [
    R("Debashis Ghoshal","uttar-pradesh","kanpur","IIT Kanpur","IIT","Physics","ghoshal@iitk.ac.in","String Theory, Field Theory, Mathematical Physics","https://home.iitk.ac.in/~ghoshal"),
    R("H. C. Verma","uttar-pradesh","kanpur","IIT Kanpur","IIT","Physics","hcverma@iitk.ac.in","Nuclear Physics, Physics Education, Experimental Physics","https://home.iitk.ac.in/~hcverma"),
    R("Kallol Mukherjee","uttar-pradesh","kanpur","IIT Kanpur","IIT","Physics","kallolm@iitk.ac.in","Condensed Matter, Quantum Materials, Spintronics","https://home.iitk.ac.in/~kallolm"),
    R("Krishnendu Sengupta","uttar-pradesh","kanpur","IIT Kanpur","IIT","Physics","ksen@iitk.ac.in","Condensed Matter Theory, Non-equilibrium Physics, Topology","https://home.iitk.ac.in/~ksen"),
    R("Rajesh Bhatt","uttar-pradesh","kanpur","IIT Kanpur","IIT","Physics","rbhatt@iitk.ac.in","Quantum Computing, Many-body Physics, Lattice Gauge Theory","https://home.iitk.ac.in/~rbhatt"),
    R("Sanjay Puri","uttar-pradesh","kanpur","IIT Kanpur","IIT","Physics","spuri@iitk.ac.in","Computational Physics, Phase Transitions, Soft Matter","https://home.iitk.ac.in/~spuri"),
    R("Subroto Mukerjee","uttar-pradesh","kanpur","IIT Kanpur","IIT","Physics","subroto@iitk.ac.in","Condensed Matter, Topological Phases, Transport","https://home.iitk.ac.in/~subroto"),
]

# =============================================================================
# IIT KHARAGPUR — EE, Maths, Physics, ME, Chemical
# =============================================================================
ALLDEPT_DATA["iits/west-bengal/kharagpur/iit-kharagpur_ee"] = [
    R("Amit Patra","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","amitpatra@ece.iitkgp.ac.in","VLSI Design, Mixed Signal Circuits, Embedded Systems","https://www.ecdept.iitkgp.ac.in/faculty/AMITPATRA"),
    R("Aurobinda Routray","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","aroutray@ee.iitkgp.ac.in","Signal Processing, BCI, Computer Vision","https://www.ee.iitkgp.ac.in/faculty/AROUTRAY"),
    R("Debashis Chatterjee","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","dc@ee.iitkgp.ac.in","Electric Machines, Power Electronics, Drives","https://www.ee.iitkgp.ac.in/faculty/DC"),
    R("Goutam Saha","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","gsaha@ece.iitkgp.ac.in","Speech Processing, Biomedical Signal Processing, NLP","https://www.ecdept.iitkgp.ac.in/faculty/GSAHA"),
    R("Mrityunjoy Chakraborty","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","mrityunjoy@ece.iitkgp.ac.in","Signal Processing, Adaptive Filtering, VLSI","https://www.ecdept.iitkgp.ac.in/faculty/MRITYUNJOY"),
    R("Partha Bhattacharyya","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","pb@ece.iitkgp.ac.in","Nanoelectronics, Semiconductor Devices, Nanosensors","https://www.ecdept.iitkgp.ac.in/faculty/PB"),
    R("Rajesh Kumar Pal","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","rkpal@ee.iitkgp.ac.in","Power Systems, Smart Grid, FACTS","https://www.ee.iitkgp.ac.in/faculty/RKPAL"),
    R("Saswat Chakrabarti","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","saswat@ece.iitkgp.ac.in","Wireless Communications, Cognitive Radio, OFDM","https://www.ecdept.iitkgp.ac.in/faculty/SASWAT"),
    R("Sudip Misra","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","smisra@cse.iitkgp.ac.in","IoT, Wireless Sensor Networks, Fog Computing","https://cse.iitkgp.ac.in/~smisra"),
    R("Tapas Samanta","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","tapas@ece.iitkgp.ac.in","Photonic Devices, Optical Communication, Nanophotonics","https://www.ecdept.iitkgp.ac.in/faculty/TAPAS"),
]

ALLDEPT_DATA["iits/west-bengal/kharagpur/iit-kharagpur_math"] = [
    R("Apala Majumdar","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","apala@maths.iitkgp.ac.in","Applied Mathematics, Liquid Crystals, PDEs","https://maths.iitkgp.ac.in/~apala"),
    R("Debasis Mitra","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","dmitra@maths.iitkgp.ac.in","Optimization, Algorithms, Scheduling","https://maths.iitkgp.ac.in/~dmitra"),
    R("Jyotsna Dutta Moulick","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","jdm@maths.iitkgp.ac.in","Coding Theory, Information Theory, Cryptography","https://maths.iitkgp.ac.in/~jdm"),
    R("Kaushik Bal","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","kbal@maths.iitkgp.ac.in","Nonlinear Analysis, Variational Methods, PDEs","https://maths.iitkgp.ac.in/~kbal"),
    R("Projesh Nath Choudhury","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","pnc@maths.iitkgp.ac.in","Matrix Analysis, Linear Algebra, Combinatorics","https://maths.iitkgp.ac.in/~pnc"),
    R("Rekha P. Kulkarni","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","rekha@maths.iitkgp.ac.in","Numerical Analysis, Integral Equations, Approximation Theory","https://maths.iitkgp.ac.in/~rekha"),
    R("Soumyendu Raha","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","sraha@maths.iitkgp.ac.in","Scientific Computing, Simulation, Differential Equations","https://maths.iitkgp.ac.in/~sraha"),
    R("Sourav Pal","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","souravpal@maths.iitkgp.ac.in","Operator Theory, Functional Analysis, Control Theory","https://maths.iitkgp.ac.in/~souravpal"),
    R("Subhamoy Maitra","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","subho@isical.ac.in","Cryptography, Boolean Functions, Stream Ciphers","https://maths.iitkgp.ac.in/~subho"),
    R("Tanmay Inamdar","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","tinamdar@maths.iitkgp.ac.in","Set Theory, Combinatorics, Graph Theory","https://maths.iitkgp.ac.in/~tinamdar"),
]

ALLDEPT_DATA["iits/west-bengal/kharagpur/iit-kharagpur_physics"] = [
    R("Anirban Mitra","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","amitra@phy.iitkgp.ac.in","Condensed Matter, Magnetism, Strongly Correlated Systems","https://phy.iitkgp.ac.in/~amitra"),
    R("Dipankar Home","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","dhome@bose.res.in","Quantum Foundations, Quantum Information, Bell Inequalities","https://phy.iitkgp.ac.in/~dhome"),
    R("Navinder Singh","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","nsingh@phy.iitkgp.ac.in","Quantum Computing, Topological Materials, Spintronics","https://phy.iitkgp.ac.in/~nsingh"),
    R("Pinaki Majumdar","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","pinaki@hri.res.in","Condensed Matter, Strongly Correlated Electrons, Numerical Methods","https://phy.iitkgp.ac.in/~pinaki"),
    R("Ritesh Kumar Singh","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","ritesh@phy.iitkgp.ac.in","Laser Physics, Ultrafast Optics, Photonics","https://phy.iitkgp.ac.in/~ritesh"),
    R("Subhasis Ghosh","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","sghosh@phy.iitkgp.ac.in","Nuclear Physics, Particle Physics, Heavy Ion Collisions","https://phy.iitkgp.ac.in/~sghosh"),
    R("Tapas Kumar Pal","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","tkpal@phy.iitkgp.ac.in","Biophysics, Protein Folding, Computational Biology","https://phy.iitkgp.ac.in/~tkpal"),
]

# =============================================================================
# IIT ROORKEE — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["iits/uttarakhand/roorkee/iit-roorkee_ee"] = [
    R("Anand Srivastava","uttarakhand","roorkee","IIT Roorkee","IIT","EE","anand.srivastava@ece.iitr.ac.in","Optical Communications, Photonics, Fiber Sensors","https://faculty.iitr.ac.in/~anandsri"),
    R("Brejesh Lall","uttarakhand","roorkee","IIT Roorkee","IIT","EE","brejesh@ece.iitr.ac.in","Multimedia Processing, Video Analysis, Computer Vision","https://faculty.iitr.ac.in/~brejesh"),
    R("Kapil Gupta","uttarakhand","roorkee","IIT Roorkee","IIT","EE","kapilg@ece.iitr.ac.in","VLSI Design, Mixed Signal Circuits","https://faculty.iitr.ac.in/~kapilg"),
    R("Laxmidhar Behera","uttarakhand","roorkee","IIT Roorkee","IIT","EE","lbehera@ece.iitr.ac.in","Robotics, Intelligent Control, Neural Networks","https://faculty.iitr.ac.in/~lbehera"),
    R("Manoj Kumar Panda","uttarakhand","roorkee","IIT Roorkee","IIT","EE","mkpanda@ece.iitr.ac.in","Power Electronics, Motor Drives, Renewable Energy","https://faculty.iitr.ac.in/~mkpanda"),
    R("Nand Kishore Garg","uttarakhand","roorkee","IIT Roorkee","IIT","EE","nkgarg@ece.iitr.ac.in","Wireless Communication, OFDM, 5G","https://faculty.iitr.ac.in/~nkgarg"),
    R("Soumya Ranjan Nayak","uttarakhand","roorkee","IIT Roorkee","IIT","EE","srnayak@ece.iitr.ac.in","Image Processing, Deep Learning, Remote Sensing","https://faculty.iitr.ac.in/~srnayak"),
    R("Vimal Bhatia","uttarakhand","roorkee","IIT Roorkee","IIT","EE","vbhatia@ece.iitr.ac.in","Signal Processing, Machine Learning, Cognitive Radio","https://faculty.iitr.ac.in/~vbhatia"),
]

ALLDEPT_DATA["iits/uttarakhand/roorkee/iit-roorkee_math"] = [
    R("Alok Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","alok.kumar@ma.iitr.ac.in","Fluid Mechanics, PDEs, Applied Mathematics","https://ma.iitr.ac.in/~alok"),
    R("Aparna Mehra","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","aparna.mehra@ma.iitr.ac.in","Fuzzy Sets, Optimization, Decision Making","https://ma.iitr.ac.in/~aparna"),
    R("Debashis Kushvah","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","dkushvah@ma.iitr.ac.in","Celestial Mechanics, Dynamical Systems","https://ma.iitr.ac.in/~dkushvah"),
    R("Nachiketa Mishra","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","nmishra@ma.iitr.ac.in","Statistics, Data Science, Machine Learning","https://ma.iitr.ac.in/~nmishra"),
    R("Pankaj Jain","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","pankaj.jain@ma.iitr.ac.in","Functional Analysis, Inequalities, Integral Operators","https://ma.iitr.ac.in/~pankajj"),
    R("Rakesh Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","rakesh@ma.iitr.ac.in","Operations Research, Queuing Theory, Stochastic Modeling","https://ma.iitr.ac.in/~rakesh"),
    R("Santosh Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","skumar@ma.iitr.ac.in","Numerical Analysis, Differential Equations, Scientific Computing","https://ma.iitr.ac.in/~skumar"),
    R("Tanvir Ali","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","tanvir.ali@ma.iitr.ac.in","Approximation Theory, Wavelets, Functional Analysis","https://ma.iitr.ac.in/~tanvir"),
]

ALLDEPT_DATA["iits/uttarakhand/roorkee/iit-roorkee_physics"] = [
    R("Amit Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","amitkr@ph.iitr.ac.in","Quantum Information, Atom Optics, Cold Atoms","https://ph.iitr.ac.in/~amitkr"),
    R("Bikash Chandra Das","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","bikash@ph.iitr.ac.in","Condensed Matter, Nanostructures, Transport","https://ph.iitr.ac.in/~bikash"),
    R("Piyush Kumar Sharma","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","pksharma@ph.iitr.ac.in","Plasma Physics, Fusion, Computational Methods","https://ph.iitr.ac.in/~pksharma"),
    R("Sandeep Kumar Dey","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","skdey@ph.iitr.ac.in","Quantum Computing, Quantum Optics, Laser Physics","https://ph.iitr.ac.in/~skdey"),
    R("Vivek Tiwari","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","vtiwari@ph.iitr.ac.in","Ultrafast Spectroscopy, Quantum Dynamics, Energy Transfer","https://ph.iitr.ac.in/~vtiwari"),
]

# =============================================================================
# IIT GUWAHATI — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["iits/assam/guwahati/iit-guwahati_ee"] = [
    R("Anil Mahanta","assam","guwahati","IIT Guwahati","IIT","EE","anil@iitg.ac.in","Signal Processing, Machine Learning, Speech","https://www.iitg.ac.in/anil"),
    R("Animesh Misra","assam","guwahati","IIT Guwahati","IIT","EE","amishrav@iitg.ac.in","Wireless Communications, Cellular Networks, Spectrum","https://www.iitg.ac.in/amishrav"),
    R("Chandan Kumar Sarkar","assam","guwahati","IIT Guwahati","IIT","EE","cksarkar@iitg.ac.in","Semiconductor Devices, VLSI, Nanoelectronics","https://www.iitg.ac.in/cksarkar"),
    R("Gaurav Trivedi","assam","guwahati","IIT Guwahati","IIT","EE","gtrivedi@iitg.ac.in","VLSI, Embedded Systems, Low Power Design","https://www.iitg.ac.in/gtrivedi"),
    R("Hiren Kumar Deva Sarma","assam","guwahati","IIT Guwahati","IIT","EE","hkds@iitg.ac.in","Optical Fiber Communication, Photonics","https://www.iitg.ac.in/hkds"),
    R("Prabin Kumar Bora","assam","guwahati","IIT Guwahati","IIT","EE","pkb@iitg.ac.in","Signal Processing, Video Coding, Multimedia","https://www.iitg.ac.in/pkb"),
    R("Shaik Sahul Hameed","assam","guwahati","IIT Guwahati","IIT","EE","shaik@iitg.ac.in","Power Systems, Smart Grid, FACTS","https://www.iitg.ac.in/shaik"),
    R("Subhranshu Sekhar Rana","assam","guwahati","IIT Guwahati","IIT","EE","ssrana@iitg.ac.in","RF and Microwave Engineering, Antenna Design","https://www.iitg.ac.in/ssrana"),
]

ALLDEPT_DATA["iits/assam/guwahati/iit-guwahati_math"] = [
    R("Amindya Banerji","assam","guwahati","IIT Guwahati","IIT","Mathematics","amindya@iitg.ac.in","Complex Analysis, Several Complex Variables","https://www.iitg.ac.in/amindya"),
    R("Anupam Saikia","assam","guwahati","IIT Guwahati","IIT","Mathematics","anupam@iitg.ac.in","Number Theory, Algebraic Number Theory, Cryptography","https://www.iitg.ac.in/anupam"),
    R("Gyan Prakash Tripathi","assam","guwahati","IIT Guwahati","IIT","Mathematics","gpt@iitg.ac.in","Number Theory, Automorphic Forms, L-functions","https://www.iitg.ac.in/gpt"),
    R("Jitendriya Swain","assam","guwahati","IIT Guwahati","IIT","Mathematics","jswain@iitg.ac.in","Harmonic Analysis, Lie Groups, Representation Theory","https://www.iitg.ac.in/jswain"),
    R("Manimaran Somasundaram","assam","guwahati","IIT Guwahati","IIT","Mathematics","mani@iitg.ac.in","PDEs, Control Theory, Controllability","https://www.iitg.ac.in/mani"),
    R("Rajen Kumar Sinha","assam","guwahati","IIT Guwahati","IIT","Mathematics","rksinha@iitg.ac.in","Numerical Methods, Finite Element Methods, PDEs","https://www.iitg.ac.in/rksinha"),
    R("Sriparna Bandyopadhyay","assam","guwahati","IIT Guwahati","IIT","Mathematics","sriparna@iitg.ac.in","Statistics, Biostatistics, Data Analysis","https://www.iitg.ac.in/sriparna"),
    R("Sudipta Dutta","assam","guwahati","IIT Guwahati","IIT","Mathematics","sdutta@iitg.ac.in","Banach Spaces, Geometry of Banach Spaces, Operator Theory","https://www.iitg.ac.in/sdutta"),
]

ALLDEPT_DATA["iits/assam/guwahati/iit-guwahati_physics"] = [
    R("Amarjyoti Mahanta","assam","guwahati","IIT Guwahati","IIT","Physics","amarjyoti@iitg.ac.in","Quantum Field Theory, Particle Physics, String Theory","https://www.iitg.ac.in/amarjyoti"),
    R("Anushree Roy","assam","guwahati","IIT Guwahati","IIT","Physics","anushree@iitg.ac.in","Experimental Condensed Matter, Magnetism, Spectroscopy","https://www.iitg.ac.in/anushree"),
    R("Bichitra Nanda Jha","assam","guwahati","IIT Guwahati","IIT","Physics","bnjha@iitg.ac.in","Plasma Physics, Laser Plasma Interaction","https://www.iitg.ac.in/bnjha"),
    R("Manabendra Nath Bera","assam","guwahati","IIT Guwahati","IIT","Physics","mnbera@iitg.ac.in","Quantum Thermodynamics, Quantum Information, Open Systems","https://www.iitg.ac.in/mnbera"),
    R("Partha P. Dey","assam","guwahati","IIT Guwahati","IIT","Physics","ppdey@iitg.ac.in","Soft Matter, Biophysics, Polymers","https://www.iitg.ac.in/ppdey"),
    R("Poulose Poulose","assam","guwahati","IIT Guwahati","IIT","Physics","poulose@iitg.ac.in","High Energy Physics, LHC Phenomenology, Beyond SM","https://www.iitg.ac.in/poulose"),
]

# =============================================================================
# IIT HYDERABAD — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["iits/telangana/hyderabad/iit-hyderabad_ee"] = [
    R("Abhinav Kumar","telangana","hyderabad","IIT Hyderabad","IIT","EE","abhinavk@ee.iith.ac.in","Wireless Communications, Massive MIMO, 5G","https://iith.ac.in/ee/abhinavk"),
    R("Amit Acharyya","telangana","hyderabad","IIT Hyderabad","IIT","EE","amitac@ee.iith.ac.in","VLSI Design, Wearable Computing, Biomedical Circuits","https://iith.ac.in/ee/amitac"),
    R("Asudeb Dutta","telangana","hyderabad","IIT Hyderabad","IIT","EE","asudeb@ee.iith.ac.in","Analog and Mixed Signal Circuits, ADC, VLSI","https://iith.ac.in/ee/asudeb"),
    R("Kiran Kuchi","telangana","hyderabad","IIT Hyderabad","IIT","EE","kkuchi@ee.iith.ac.in","Wireless Communications, LTE, 5G NR","https://iith.ac.in/ee/kkuchi"),
    R("Mohan Raghavan","telangana","hyderabad","IIT Hyderabad","IIT","EE","mohanr@ee.iith.ac.in","RF Circuits, Millimeter Wave, Power Amplifiers","https://iith.ac.in/ee/mohanr"),
    R("P. K. Baruah","telangana","hyderabad","IIT Hyderabad","IIT","EE","pkbaruah@ee.iith.ac.in","Power Systems, Smart Grid, Distributed Generation","https://iith.ac.in/ee/pkbaruah"),
    R("Santhosh Kumar Chede","telangana","hyderabad","IIT Hyderabad","IIT","EE","santhosh@ee.iith.ac.in","Signal Processing, Medical Imaging, Machine Learning","https://iith.ac.in/ee/santhosh"),
    R("Sumohana Channappayya","telangana","hyderabad","IIT Hyderabad","IIT","EE","sumohana@ee.iith.ac.in","Image Quality Assessment, Computer Vision, Deep Learning","https://iith.ac.in/ee/sumohana"),
]

ALLDEPT_DATA["iits/telangana/hyderabad/iit-hyderabad_math"] = [
    R("A. Satyanarayana Reddy","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","satya@math.iith.ac.in","Numerical Analysis, Parallel Computation, PDEs","https://math.iith.ac.in/~satya"),
    R("Balasubramanian Sriram","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","bsriram@math.iith.ac.in","Probability, Statistics, Stochastic Processes","https://math.iith.ac.in/~bsriram"),
    R("Girja Shanker Sahay","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","gsahay@math.iith.ac.in","Algebraic Topology, Differential Geometry","https://math.iith.ac.in/~gsahay"),
    R("Mythily Ramaswamy","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","mythily@math.iith.ac.in","Control Theory, PDEs, Optimal Control","https://math.iith.ac.in/~mythily"),
    R("Rajendra Srivastava","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","rajendra@math.iith.ac.in","Operations Research, Optimization, Game Theory","https://math.iith.ac.in/~rajendra"),
    R("Seshadri Sivakumar","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","seshadri@math.iith.ac.in","Combinatorics, Graph Theory, Algorithms","https://math.iith.ac.in/~seshadri"),
    R("Soumyabrata Chakraborty","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","soumyab@math.iith.ac.in","Machine Learning, Statistical Learning Theory","https://math.iith.ac.in/~soumyab"),
]

ALLDEPT_DATA["iits/telangana/hyderabad/iit-hyderabad_physics"] = [
    R("Jasleen Lugani","telangana","hyderabad","IIT Hyderabad","IIT","Physics","jasleen@phy.iith.ac.in","Quantum Computing, Quantum Optics, Photonics","https://iith.ac.in/phy/jasleen"),
    R("K. V. Adarsh","telangana","hyderabad","IIT Hyderabad","IIT","Physics","adarsh@phy.iith.ac.in","Nanostructures, Photonics, Ultrafast Spectroscopy","https://iith.ac.in/phy/adarsh"),
    R("Ratheesh Kumar Meleppat","telangana","hyderabad","IIT Hyderabad","IIT","Physics","ratheesh@phy.iith.ac.in","Optical Coherence Tomography, Biophotonics","https://iith.ac.in/phy/ratheesh"),
    R("Saurabh Basu","telangana","hyderabad","IIT Hyderabad","IIT","Physics","sbasu@phy.iith.ac.in","Condensed Matter Theory, Quantum Many-body Physics","https://iith.ac.in/phy/sbasu"),
    R("Suresh Govindarajan","telangana","hyderabad","IIT Hyderabad","IIT","Physics","sureshg@phy.iith.ac.in","String Theory, Mathematical Physics, Moonshine","https://iith.ac.in/phy/sureshg"),
]

# =============================================================================
# IIT INDORE — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["iits/madhya-pradesh/indore/iit-indore_ee"] = [
    R("Amit Sethi","madhya-pradesh","indore","IIT Indore","IIT","EE","asethi@iiti.ac.in","Medical Imaging, Computer Vision, Deep Learning","https://people.iiti.ac.in/~asethi"),
    R("Kapil Ahuja","madhya-pradesh","indore","IIT Indore","IIT","EE","kahuja@iiti.ac.in","Scientific Computing, Model Reduction, Machine Learning","https://people.iiti.ac.in/~kahuja"),
    R("Neelesh Kumar","madhya-pradesh","indore","IIT Indore","IIT","EE","nkumar@iiti.ac.in","Wireless Communications, Cooperative Networks, NOMA","https://people.iiti.ac.in/~nkumar"),
    R("Puneet Gupta","madhya-pradesh","indore","IIT Indore","IIT","EE","pgupta@iiti.ac.in","Signal Processing, Radar, Machine Learning","https://people.iiti.ac.in/~pgupta"),
    R("Santosh Kumar Vishvakarma","madhya-pradesh","indore","IIT Indore","IIT","EE","skvishvakarma@iiti.ac.in","VLSI, Low Power Circuits, Nanoelectronics","https://people.iiti.ac.in/~skvishvakarma"),
    R("Samarendra Dandapat","madhya-pradesh","indore","IIT Indore","IIT","EE","sdandapat@iiti.ac.in","Biomedical Signal Processing, ECG, EEG, Machine Learning","https://people.iiti.ac.in/~sdandapat"),
]

ALLDEPT_DATA["iits/madhya-pradesh/indore/iit-indore_math"] = [
    R("Absos Ali Shaikh","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","aashaikh@iiti.ac.in","Differential Geometry, Riemannian Manifolds","https://people.iiti.ac.in/~aashaikh"),
    R("Biplab Basak","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","bbasak@iiti.ac.in","Algebraic Topology, Combinatorics, Discrete Geometry","https://people.iiti.ac.in/~bbasak"),
    R("Dhiman Mallick","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","dmallick@iiti.ac.in","Statistics, Probability, Stochastic Processes","https://people.iiti.ac.in/~dmallick"),
    R("Harish Chandra","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","hchandra@iiti.ac.in","Optimization, Operations Research, Game Theory","https://people.iiti.ac.in/~hchandra"),
    R("Neha Gupta","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","ngupta@iiti.ac.in","Numerical Analysis, Computational Mathematics, PDEs","https://people.iiti.ac.in/~ngupta"),
    R("Soumya Dey","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","sdey@iiti.ac.in","Knot Theory, Topology, 3-Manifolds","https://people.iiti.ac.in/~sdey"),
]

ALLDEPT_DATA["iits/madhya-pradesh/indore/iit-indore_physics"] = [
    R("Arun Kumar Pati","madhya-pradesh","indore","IIT Indore","IIT","Physics","akpati@iiti.ac.in","Quantum Information, Quantum Computing, Entanglement","https://people.iiti.ac.in/~akpati"),
    R("C. M. Bhatt","madhya-pradesh","indore","IIT Indore","IIT","Physics","cmbhatt@iiti.ac.in","Geophysics, Remote Sensing, Disaster Monitoring","https://people.iiti.ac.in/~cmbhatt"),
    R("Mayuri Prasad","madhya-pradesh","indore","IIT Indore","IIT","Physics","mprasad@iiti.ac.in","Nanophotonics, Plasmonics, Optical Sensors","https://people.iiti.ac.in/~mprasad"),
    R("Pranab Kumar Mandal","madhya-pradesh","indore","IIT Indore","IIT","Physics","pkmandal@iiti.ac.in","Condensed Matter, Spintronics, Magnetics","https://people.iiti.ac.in/~pkmandal"),
]

# =============================================================================
# IIT GANDHINAGAR — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["iits/gujarat/gandhinagar/iit-gandhinagar_ee"] = [
    R("Amit Acharyya","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","amitac@iitgn.ac.in","VLSI, Wearable IoT, Edge AI","https://iitgn.ac.in/faculty/ee/amitac"),
    R("Himanshu Shekhar","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","himanshu.shekhar@iitgn.ac.in","Ultrasound Imaging, Biomedical Instrumentation","https://iitgn.ac.in/faculty/ee/himanshu"),
    R("Malay Shah","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","malay.shah@iitgn.ac.in","Power Systems, Smart Grid, Renewable Energy Integration","https://iitgn.ac.in/faculty/ee/malay"),
    R("Nitin Khanna","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","nitin.khanna@iitgn.ac.in","Image Processing, Forensics, Steganography, AI","https://iitgn.ac.in/faculty/ee/nitin"),
    R("Prabhat Mishra","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","prabhat.mishra@iitgn.ac.in","Embedded Systems, FPGA, Hardware Security","https://iitgn.ac.in/faculty/ee/prabhat"),
    R("Sai Guruva Reddy","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","saiguruva@iitgn.ac.in","Computer Vision, Autonomous Vehicles, Robotics","https://iitgn.ac.in/faculty/ee/saiguruva"),
]

ALLDEPT_DATA["iits/gujarat/gandhinagar/iit-gandhinagar_math"] = [
    R("Amit Setia","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","amit.setia@iitgn.ac.in","Numerical Analysis, PDEs, Scientific Computing","https://iitgn.ac.in/faculty/math/amit"),
    R("Anjan Kumar Chakraborty","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","anjan.chakraborty@iitgn.ac.in","Algebra, Combinatorics, Graph Theory","https://iitgn.ac.in/faculty/math/anjan"),
    R("Debasis Kundu","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","debasis.kundu@iitgn.ac.in","Statistics, Data Analysis, Signal Processing","https://iitgn.ac.in/faculty/math/debasis"),
    R("Indranil Biswas","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","indranil@iitgn.ac.in","Algebraic Geometry, Vector Bundles","https://iitgn.ac.in/faculty/math/indranil"),
    R("Krishnamurthi Ravishankar","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","ravi@iitgn.ac.in","Probability, Stochastic Processes, Mathematical Finance","https://iitgn.ac.in/faculty/math/ravi"),
]

ALLDEPT_DATA["iits/gujarat/gandhinagar/iit-gandhinagar_physics"] = [
    R("Aveek Bid","gujarat","gandhinagar","IIT Gandhinagar","IIT","Physics","aveek.bid@iitgn.ac.in","Quantum Transport, 2D Materials, Mesoscopic Physics","https://iitgn.ac.in/faculty/phy/aveek"),
    R("Debdeep Jena","gujarat","gandhinagar","IIT Gandhinagar","IIT","Physics","debdeep@iitgn.ac.in","Semiconductor Physics, 2D Materials, Power Electronics","https://iitgn.ac.in/faculty/phy/debdeep"),
    R("Manan Shah","gujarat","gandhinagar","IIT Gandhinagar","IIT","Physics","manan.shah@iitgn.ac.in","Chemical Engineering, Nanotechnology, Materials","https://iitgn.ac.in/faculty/phy/manan"),
    R("Sudipta Sarangi","gujarat","gandhinagar","IIT Gandhinagar","IIT","Physics","sudipta@iitgn.ac.in","Condensed Matter, Lattice Dynamics, Phonons","https://iitgn.ac.in/faculty/phy/sudipta"),
]

# =============================================================================
# IIT JODHPUR — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["iits/rajasthan/jodhpur/iit-jodhpur_ee"] = [
    R("Aditya Nigam","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","adityan@iitj.ac.in","Biometrics, Computer Vision, Deep Learning","https://iitj.ac.in/faculty/index.php?lid=adityan"),
    R("Apurba Das","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","apurbadas@iitj.ac.in","VLSI, Digital Design, Computer Architecture","https://iitj.ac.in/faculty/index.php?lid=apurbadas"),
    R("Braj Bhushan Lohia","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","bblohia@iitj.ac.in","RF Microwave, Antenna, Wireless","https://iitj.ac.in/faculty/index.php?lid=bblohia"),
    R("Santanu Chaudhury","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","schaudhury@iitj.ac.in","Computer Vision, AR/VR, AI","https://iitj.ac.in/faculty/index.php?lid=schaudhury"),
    R("Surendra Prasad","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","surendra@iitj.ac.in","Signal Processing, Array Processing, Statistical Signal","https://iitj.ac.in/faculty/index.php?lid=surendra"),
    R("Vivek Bohara","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","vbohara@iitj.ac.in","Full Duplex Radio, Interference Management, 5G/6G","https://iitj.ac.in/faculty/index.php?lid=vbohara"),
]

ALLDEPT_DATA["iits/rajasthan/jodhpur/iit-jodhpur_math"] = [
    R("Bankteshwar Tiwari","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","btiwari@iitj.ac.in","Differential Geometry, Finsler Geometry","https://iitj.ac.in/faculty/index.php?lid=btiwari"),
    R("Kamal Lochan Patra","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","klpatra@iitj.ac.in","Matrix Theory, Linear Algebra, Operator Theory","https://iitj.ac.in/faculty/index.php?lid=klpatra"),
    R("Pankaj Joshi","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","pjoshi@iitj.ac.in","Probability, Statistics, Actuarial Science","https://iitj.ac.in/faculty/index.php?lid=pjoshi"),
    R("Ratan Kumar Giri","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","rkgiri@iitj.ac.in","PDEs, Scattering Theory, Spectral Theory","https://iitj.ac.in/faculty/index.php?lid=rkgiri"),
]

ALLDEPT_DATA["iits/rajasthan/jodhpur/iit-jodhpur_physics"] = [
    R("Anand Vikram Singh","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","avsingh@iitj.ac.in","Nanomaterials, Biosensors, Nanofabrication","https://iitj.ac.in/faculty/index.php?lid=avsingh"),
    R("Bikash Kumar Behera","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","bkbehera@iitj.ac.in","Quantum Computing, Quantum Error Correction, NMR","https://iitj.ac.in/faculty/index.php?lid=bkbehera"),
    R("Subhadeep De","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","sde@iitj.ac.in","Quantum Optics, Laser Cooling, Cold Atoms","https://iitj.ac.in/faculty/index.php?lid=sde"),
]

# =============================================================================
# IIT ROPAR — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["iits/punjab/ropar/iit-ropar_ee"] = [
    R("Bhupendra Nath Tiwari","punjab","ropar","IIT Ropar","IIT","EE","bntiwari@iitrpr.ac.in","Wireless Communications, Channel Coding, 5G","https://www.iitrpr.ac.in/bntiwari"),
    R("Girdhari Lal","punjab","ropar","IIT Ropar","IIT","EE","girdhari@iitrpr.ac.in","Signal Processing, Machine Learning, Biomedical","https://www.iitrpr.ac.in/girdhari"),
    R("Harish Kumar","punjab","ropar","IIT Ropar","IIT","EE","harishk@iitrpr.ac.in","Power Electronics, Motor Drives, Renewable Energy","https://www.iitrpr.ac.in/harishk"),
    R("Neeraj Kumar","punjab","ropar","IIT Ropar","IIT","EE","neerajkumar@iitrpr.ac.in","Computer Vision, Medical Imaging, Deep Learning","https://www.iitrpr.ac.in/neerajkumar"),
    R("Surender Kumar Sharma","punjab","ropar","IIT Ropar","IIT","EE","sksharma@iitrpr.ac.in","VLSI, Digital Electronics, Reconfigurable Computing","https://www.iitrpr.ac.in/sksharma"),
]

ALLDEPT_DATA["iits/punjab/ropar/iit-ropar_math"] = [
    R("Anoop Kumar","punjab","ropar","IIT Ropar","IIT","Mathematics","anoopkumar@iitrpr.ac.in","Functional Analysis, Operator Theory","https://www.iitrpr.ac.in/anoopkumar"),
    R("Dinesh Kumar","punjab","ropar","IIT Ropar","IIT","Mathematics","dineshkumar@iitrpr.ac.in","Statistics, Statistical Inference, Survival Analysis","https://www.iitrpr.ac.in/dineshkumar"),
    R("Kushal K. Dey","punjab","ropar","IIT Ropar","IIT","Mathematics","kkdey@iitrpr.ac.in","Statistical Genomics, Machine Learning for Biology","https://www.iitrpr.ac.in/kkdey"),
    R("Sunil Kumar","punjab","ropar","IIT Ropar","IIT","Mathematics","sunilkumar@iitrpr.ac.in","Optimization, Operations Research, Scheduling","https://www.iitrpr.ac.in/sunilkumar"),
]

# =============================================================================
# IIT PATNA — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["iits/bihar/patna/iit-patna_ee"] = [
    R("Anil Kumar Tiwari","bihar","patna","IIT Patna","IIT","EE","aktiwari@iitp.ac.in","Wireless Sensor Networks, IoT, Vehicular Networks","https://www.iitp.ac.in/~aktiwari"),
    R("Bhaskar Gupta","bihar","patna","IIT Patna","IIT","EE","bgupta@iitp.ac.in","RF Microwave, Antenna, Metamaterials","https://www.iitp.ac.in/~bgupta"),
    R("Kailash Chandra Ray","bihar","patna","IIT Patna","IIT","EE","kcray@iitp.ac.in","VLSI, Mixed Signal Circuits, Digital Signal Processing","https://www.iitp.ac.in/~kcray"),
    R("Rajveer Singh Yaduvanshi","bihar","patna","IIT Patna","IIT","EE","rsyaduvanshi@iitp.ac.in","Antenna Design, MIMO, 5G","https://www.iitp.ac.in/~rsyaduvanshi"),
    R("Subhankar Ghosh","bihar","patna","IIT Patna","IIT","EE","sghosh@iitp.ac.in","Computer Vision, Deep Learning, Medical AI","https://www.iitp.ac.in/~sghosh"),
]

ALLDEPT_DATA["iits/bihar/patna/iit-patna_math"] = [
    R("Akhilesh Kumar Dubey","bihar","patna","IIT Patna","IIT","Mathematics","akdubey@iitp.ac.in","Number Theory, Algebraic Number Theory","https://www.iitp.ac.in/~akdubey"),
    R("Biswajit Bhattacharyya","bihar","patna","IIT Patna","IIT","Mathematics","bbhatt@iitp.ac.in","Statistics, Probability, Bayesian Analysis","https://www.iitp.ac.in/~bbhatt"),
    R("Rajib Mall","bihar","patna","IIT Patna","IIT","Mathematics","mall@iitp.ac.in","Real Analysis, Measure Theory, Topology","https://www.iitp.ac.in/~mall"),
    R("Sandeep Kumar","bihar","patna","IIT Patna","IIT","Mathematics","skumar@iitp.ac.in","Optimization, Game Theory, Operations Research","https://www.iitp.ac.in/~skumar"),
]

# =============================================================================
# IIT BHU VARANASI — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["iits/uttar-pradesh/varanasi/iit-bhu_ee"] = [
    R("Aditya Trivedi","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","EE","aditya.ece@iitbhu.ac.in","Wireless Networks, Cognitive Radio, OFDM","https://www.iitbhu.ac.in/dept/ece/people/adityaece"),
    R("Bharat Singh","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","EE","bharats.ece@iitbhu.ac.in","Signal Processing, Array Antennas, MIMO","https://www.iitbhu.ac.in/dept/ece/people/bharatsece"),
    R("D. K. Lobiyal","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","EE","dklobiyal.ece@iitbhu.ac.in","Ad-hoc Networks, VANETs, Vehicular IoT","https://www.iitbhu.ac.in/dept/ece/people/dklobiyalece"),
    R("M. V. Kartikeyan","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","EE","mvkartikeyan.ece@iitbhu.ac.in","Millimeter Wave, Microwave Devices, Terahertz","https://www.iitbhu.ac.in/dept/ece/people/mvkartikeyanece"),
    R("Rajeev Kumar Singh","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","EE","rksingh.ece@iitbhu.ac.in","Power Electronics, Energy Conversion, Drives","https://www.iitbhu.ac.in/dept/ece/people/rksinghece"),
    R("Sanjay Kumar Singh","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","EE","sksingh.ece@iitbhu.ac.in","VLSI, Low Power Design, Reconfigurable Computing","https://www.iitbhu.ac.in/dept/ece/people/sksinghece"),
]

ALLDEPT_DATA["iits/uttar-pradesh/varanasi/iit-bhu_math"] = [
    R("Ajay Choudhary","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Mathematics","ajaychoudhary.mat@iitbhu.ac.in","Numerical Methods, Scientific Computing, PDEs","https://www.iitbhu.ac.in/dept/mat/people/ajaychoudharymat"),
    R("Bikramaditya Datta","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Mathematics","bdatta.mat@iitbhu.ac.in","Algebra, Module Theory, Ring Theory","https://www.iitbhu.ac.in/dept/mat/people/bdattamat"),
    R("Rajesh Srivastava","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Mathematics","rsrivastava.mat@iitbhu.ac.in","Operations Research, Stochastic Modeling, Queuing","https://www.iitbhu.ac.in/dept/mat/people/rsrivastavamat"),
    R("Sunil Kumar","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Mathematics","sunilkumar.mat@iitbhu.ac.in","Topology, Functional Analysis, Banach Spaces","https://www.iitbhu.ac.in/dept/mat/people/sunilkumarmat"),
]

ALLDEPT_DATA["iits/uttar-pradesh/varanasi/iit-bhu_physics"] = [
    R("Amit Kumar Singh","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Physics","aksingh.phy@iitbhu.ac.in","Condensed Matter, Magnetic Nanomaterials, Spintronics","https://www.iitbhu.ac.in/dept/phy/people/aksinghphy"),
    R("Gyan Prakash Srivastava","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Physics","gpsrivastava.phy@iitbhu.ac.in","Computational Physics, Phonons, Materials Theory","https://www.iitbhu.ac.in/dept/phy/people/gpsrivastavaphy"),
    R("Pankaj Mishra","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Physics","pmishra.phy@iitbhu.ac.in","Soft Matter, Polymer Physics, Computational Biophysics","https://www.iitbhu.ac.in/dept/phy/people/pmishraphy"),
    R("Saurabh Saxena","uttar-pradesh","varanasi","IIT (BHU) Varanasi","IIT","Physics","ssaxena.phy@iitbhu.ac.in","Laser Spectroscopy, Atomic Physics, Quantum Optics","https://www.iitbhu.ac.in/dept/phy/people/ssaxenaphy"),
]

# =============================================================================
# NIT TRICHY — EE, Maths, Physics, Production, Chemical
# =============================================================================
ALLDEPT_DATA["nits/tamil-nadu/tiruchirappalli/nit-trichy_ee"] = [
    R("A. Amudha","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","amudha@nitt.edu","Power Electronics, Electric Drives, Renewable Energy","https://www.nitt.edu/home/academics/departments/eee/faculty/amudha"),
    R("B. Venkataramana Reddy","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","bvreddy@nitt.edu","Signal Processing, Biomedical Engineering, DSP","https://www.nitt.edu/home/academics/departments/eee/faculty/bvreddy"),
    R("C. Christober Asir Rajan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","christober@nitt.edu","Power Systems, Smart Grid, Optimization","https://www.nitt.edu/home/academics/departments/eee/faculty/christober"),
    R("K. Chitra","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","chitra@nitt.edu","Wireless Communications, OFDM, Channel Estimation","https://www.nitt.edu/home/academics/departments/ece/faculty/chitra"),
    R("M. Senthil Arumugam","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","msa@nitt.edu","Computational Intelligence, Evolutionary Algorithms, Soft Computing","https://www.nitt.edu/home/academics/departments/eee/faculty/msa"),
    R("R. Amutha","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","amutha@nitt.edu","Wireless Sensor Networks, IoT, Ad hoc Networks","https://www.nitt.edu/home/academics/departments/ece/faculty/amutha"),
    R("S. Malathi","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","malathi@nitt.edu","Computer Vision, Image Processing, Pattern Recognition","https://www.nitt.edu/home/academics/departments/ece/faculty/malathi"),
    R("T. Senthil Kumar","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","tsk@nitt.edu","VLSI, Low Power Circuits, Nano Electronics","https://www.nitt.edu/home/academics/departments/ece/faculty/tsk"),
]

ALLDEPT_DATA["nits/tamil-nadu/tiruchirappalli/nit-trichy_math"] = [
    R("A. Srinivasan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","asrinivasan@nitt.edu","Graph Theory, Combinatorics, Algebraic Graph Theory","https://www.nitt.edu/home/academics/departments/maths/faculty/asrinivasan"),
    R("B. Sundaravadivoo","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","bsundaravadivoo@nitt.edu","Fuzzy Logic, Decision Making, Operations Research","https://www.nitt.edu/home/academics/departments/maths/faculty/bsundaravadivoo"),
    R("E. Krishnarajah","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","ekrishnarajah@nitt.edu","Differential Equations, Fluid Dynamics, Mathematical Modeling","https://www.nitt.edu/home/academics/departments/maths/faculty/ekrishnarajah"),
    R("P. Balasubramaniam","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","pbalasubramaniam@nitt.edu","Stochastic Differential Equations, Control Theory, Neural Networks","https://www.nitt.edu/home/academics/departments/maths/faculty/pbalasubramaniam"),
    R("S. Santhakumar","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","santhakumar@nitt.edu","Probability, Statistics, Reliability Theory","https://www.nitt.edu/home/academics/departments/maths/faculty/santhakumar"),
    R("T. Muthukumar","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","tmuthukumar@nitt.edu","PDEs, Functional Analysis, Homogenization","https://www.nitt.edu/home/academics/departments/maths/faculty/tmuthukumar"),
]

ALLDEPT_DATA["nits/tamil-nadu/tiruchirappalli/nit-trichy_physics"] = [
    R("A. Ramanand","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","aramanand@nitt.edu","Nanomaterials, Photovoltaics, Thin Film Technology","https://www.nitt.edu/home/academics/departments/physics/faculty/aramanand"),
    R("J. Kanagathara","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","jkanagathara@nitt.edu","Crystal Growth, Nonlinear Optics, Photonics","https://www.nitt.edu/home/academics/departments/physics/faculty/jkanagathara"),
    R("M. Navaneethan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","navaneethan@nitt.edu","Semiconductor Nanostructures, Solar Cells, Photocatalysis","https://www.nitt.edu/home/academics/departments/physics/faculty/navaneethan"),
    R("P. Suresh","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","sureshp@nitt.edu","Quantum Mechanics, Computational Physics, Condensed Matter","https://www.nitt.edu/home/academics/departments/physics/faculty/sureshp"),
    R("S. Srinivasan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","ssrinivasan@nitt.edu","Laser Physics, Spectroscopy, Optical Materials","https://www.nitt.edu/home/academics/departments/physics/faculty/ssrinivasan"),
]

# =============================================================================
# NIT WARANGAL — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["nits/telangana/warangal/nit-warangal_ee"] = [
    R("A. D. Raj Kumar","telangana","warangal","NIT Warangal","NIT","EE","adrk@nitw.ac.in","Power Systems, FACTS, Smart Grid","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=19&strFacID=ADRK"),
    R("B. L. Prakasa Rao","telangana","warangal","NIT Warangal","NIT","EE","blpr@nitw.ac.in","Statistical Signal Processing, Detection, Estimation","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=19&strFacID=BLPR"),
    R("D. Srilatha","telangana","warangal","NIT Warangal","NIT","EE","srilatha@nitw.ac.in","Computer Vision, Image Processing, Machine Learning","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=19&strFacID=SRIL"),
    R("M. V. Subramanyam","telangana","warangal","NIT Warangal","NIT","EE","mvs@nitw.ac.in","Image Compression, Watermarking, Signal Processing","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=19&strFacID=MVS"),
    R("N. Srikanth","telangana","warangal","NIT Warangal","NIT","EE","srikanth@nitw.ac.in","Wireless Communications, MIMO, Cooperative Systems","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=19&strFacID=NSRI"),
    R("S. Unnikrishna Pillai","telangana","warangal","NIT Warangal","NIT","EE","pillai@nitw.ac.in","Radar Signal Processing, Detection Theory","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=19&strFacID=PILL"),
    R("Venu Madhav Kuthuri","telangana","warangal","NIT Warangal","NIT","EE","venumk@nitw.ac.in","Power Electronics, Drives, Energy Conversion","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=19&strFacID=VMK"),
]

ALLDEPT_DATA["nits/telangana/warangal/nit-warangal_math"] = [
    R("A. Benerji Babu","telangana","warangal","NIT Warangal","NIT","Mathematics","benerji@nitw.ac.in","Fluid Dynamics, PDEs, Mathematical Modeling","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=14"),
    R("D. Bhanu Prasad","telangana","warangal","NIT Warangal","NIT","Mathematics","bhanup@nitw.ac.in","Statistics, Data Analysis, Machine Learning","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=14"),
    R("G. Laxmaiah","telangana","warangal","NIT Warangal","NIT","Mathematics","laxmaiah@nitw.ac.in","Optimization, Operations Research, Graph Theory","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=14"),
    R("M. Suryanarayana","telangana","warangal","NIT Warangal","NIT","Mathematics","surya@nitw.ac.in","Algebra, Number Theory, Cryptography","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=14"),
    R("T. Mathew Varghese","telangana","warangal","NIT Warangal","NIT","Mathematics","tmv@nitw.ac.in","Topology, Functional Analysis, Fixed Point Theory","https://www.nitw.ac.in/nitwnew/facultyprofile.aspx?nDeptID=14"),
]

# =============================================================================
# NIT ROURKELA — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["nits/odisha/rourkela/nit-rourkela_ee"] = [
    R("Badri Narayan Mohapatra","odisha","rourkela","NIT Rourkela","NIT","EE","bnm@nitrkl.ac.in","Wireless Communications, Cognitive Radio, OFDM","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/bnm"),
    R("D. P. Acharya","odisha","rourkela","NIT Rourkela","NIT","EE","dpa@nitrkl.ac.in","VLSI Design, Low Power Circuits, Embedded Systems","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/dpa"),
    R("Ganapati Panda","odisha","rourkela","NIT Rourkela","NIT","EE","gpanda@nitrkl.ac.in","Signal Processing, Machine Learning, Biomedical","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/gpanda"),
    R("K. B. Mohanty","odisha","rourkela","NIT Rourkela","NIT","EE","kbm@nitrkl.ac.in","Power Electronics, Drives, Power Quality","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/kbm"),
    R("Poonam Singh","odisha","rourkela","NIT Rourkela","NIT","EE","psingh@nitrkl.ac.in","Image Processing, Computer Vision, AI","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/psingh"),
    R("Sudhansu Sekhar Singh","odisha","rourkela","NIT Rourkela","NIT","EE","sss@nitrkl.ac.in","Antenna, Microwave, Metamaterials","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/sss"),
]

ALLDEPT_DATA["nits/odisha/rourkela/nit-rourkela_math"] = [
    R("Bata Krushna Bhoi","odisha","rourkela","NIT Rourkela","NIT","Mathematics","bkbhoi@nitrkl.ac.in","Statistics, Data Science, Biostatistics","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/bkbhoi"),
    R("Jugal Mohapatra","odisha","rourkela","NIT Rourkela","NIT","Mathematics","jmohapatra@nitrkl.ac.in","Numerical Analysis, Singular Perturbation, PDEs","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/jmohapatra"),
    R("Manas Ranjan Tripathy","odisha","rourkela","NIT Rourkela","NIT","Mathematics","mrt@nitrkl.ac.in","Linear Algebra, Matrix Theory, Operator Theory","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/mrt"),
    R("Smita Rani Pati","odisha","rourkela","NIT Rourkela","NIT","Mathematics","srpati@nitrkl.ac.in","Graph Theory, Combinatorics, Domination","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/srpati"),
    R("Suvendu Ranjan Pattanaik","odisha","rourkela","NIT Rourkela","NIT","Mathematics","srp@nitrkl.ac.in","Operations Research, Optimization, Game Theory","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/srp"),
]

ALLDEPT_DATA["nits/odisha/rourkela/nit-rourkela_physics"] = [
    R("Arun Kumar Panda","odisha","rourkela","NIT Rourkela","NIT","Physics","akpanda@nitrkl.ac.in","Semiconductors, Photovoltaics, Thin Film Solar Cells","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/akpanda"),
    R("Bibhuti B. Sahoo","odisha","rourkela","NIT Rourkela","NIT","Physics","bbsahoo@nitrkl.ac.in","Condensed Matter, Strongly Correlated Systems, Magnetism","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/bbsahoo"),
    R("Brindaban Modak","odisha","rourkela","NIT Rourkela","NIT","Physics","bmodak@nitrkl.ac.in","Nuclear Physics, Theoretical Physics, Hadron Structure","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/bmodak"),
    R("Sachindra Nath Sarangi","odisha","rourkela","NIT Rourkela","NIT","Physics","snsarangi@nitrkl.ac.in","Nanomaterials, Quantum Dots, Semiconductor Nanostructures","https://www.nitrkl.ac.in/FacultyStaff/FacultyProfile/snsarangi"),
]

# =============================================================================
# NIT CALICUT — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["nits/kerala/kozhikode/nit-calicut_ee"] = [
    R("Abdulla P","kerala","kozhikode","NIT Calicut","NIT","EE","abdulla@nitc.ac.in","Power Systems, HVDC, Flexible AC Transmission","https://www.nitc.ac.in/index.php/departments/electrical-engineering/faculties"),
    R("Babu Paul","kerala","kozhikode","NIT Calicut","NIT","EE","babupaul@nitc.ac.in","Biomedical Engineering, Embedded Systems, Signal Processing","https://www.nitc.ac.in/index.php/departments/electrical-engineering/faculties"),
    R("Deepa V Jose","kerala","kozhikode","NIT Calicut","NIT","EE","deepa@nitc.ac.in","Image Processing, Computer Vision, Machine Learning","https://www.nitc.ac.in/index.php/departments/electronics-and-communication-engineering/faculties"),
    R("Gopakumar K","kerala","kozhikode","NIT Calicut","NIT","EE","gopakumark@nitc.ac.in","VLSI, Digital Design, Reconfigurable Systems","https://www.nitc.ac.in/index.php/departments/electronics-and-communication-engineering/faculties"),
    R("Jeevamma Jacob","kerala","kozhikode","NIT Calicut","NIT","EE","jeevamma@nitc.ac.in","Control Systems, Robust Control, Nonlinear Dynamics","https://www.nitc.ac.in/index.php/departments/electrical-engineering/faculties"),
    R("V. K. Govindan","kerala","kozhikode","NIT Calicut","NIT","EE","vkgovindan@nitc.ac.in","Machine Learning, Neural Networks, Computer Vision","https://www.nitc.ac.in/index.php/departments/computer-science-and-engineering/faculties"),
]

ALLDEPT_DATA["nits/kerala/kozhikode/nit-calicut_math"] = [
    R("A. Vijayakumar","kerala","kozhikode","NIT Calicut","NIT","Mathematics","avijayakumar@nitc.ac.in","Graph Theory, Combinatorics, Domination Theory","https://www.nitc.ac.in/index.php/departments/mathematics/faculties"),
    R("C. S. Lalitha","kerala","kozhikode","NIT Calicut","NIT","Mathematics","cslalitha@nitc.ac.in","Optimization, Variational Analysis, Nonlinear Programming","https://www.nitc.ac.in/index.php/departments/mathematics/faculties"),
    R("P. B. Vinodkumar","kerala","kozhikode","NIT Calicut","NIT","Mathematics","pbvinodkumar@nitc.ac.in","Algebra, Linear Algebra, Ring Theory","https://www.nitc.ac.in/index.php/departments/mathematics/faculties"),
    R("Ramesh Kumar Vinu","kerala","kozhikode","NIT Calicut","NIT","Mathematics","rameshvinu@nitc.ac.in","Statistics, Probability, Reliability Theory","https://www.nitc.ac.in/index.php/departments/mathematics/faculties"),
    R("S. Balakrishnan","kerala","kozhikode","NIT Calicut","NIT","Mathematics","sbalakrishnan@nitc.ac.in","Numerical Analysis, Computational Mathematics, ODEs","https://www.nitc.ac.in/index.php/departments/mathematics/faculties"),
]

ALLDEPT_DATA["nits/kerala/kozhikode/nit-calicut_physics"] = [
    R("B. Sankarraman","kerala","kozhikode","NIT Calicut","NIT","Physics","bsankarraman@nitc.ac.in","Photonics, Fiber Optics, Optical Sensors","https://www.nitc.ac.in/index.php/departments/physics/faculties"),
    R("K. E. Rajendra Kumar","kerala","kozhikode","NIT Calicut","NIT","Physics","kerk@nitc.ac.in","Condensed Matter, Thin Films, Semiconductor Devices","https://www.nitc.ac.in/index.php/departments/physics/faculties"),
    R("Peer Mohamed M","kerala","kozhikode","NIT Calicut","NIT","Physics","peermohamed@nitc.ac.in","Computational Physics, DFT, Materials Science","https://www.nitc.ac.in/index.php/departments/physics/faculties"),
    R("Rajan Jha","kerala","kozhikode","NIT Calicut","NIT","Physics","rajanjha@nitc.ac.in","Photonics, Nanophotonics, Surface Plasmon Resonance","https://www.nitc.ac.in/index.php/departments/physics/faculties"),
]

# =============================================================================
# NIT SURATHKAL — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["nits/karnataka/surathkal/nit-surathkal_ee"] = [
    R("Balaji Chakravarthy","karnataka","surathkal","NIT Surathkal","NIT","EE","balaji@nitk.edu.in","Power Electronics, Drives, Renewable Energy","https://eee.nitk.ac.in/faculty/balaji"),
    R("Dattatraya Kalale","karnataka","surathkal","NIT Surathkal","NIT","EE","dattatraya@nitk.edu.in","Power Systems, Protection, Smart Grid","https://eee.nitk.ac.in/faculty/dattatraya"),
    R("H. V. Govindaraju","karnataka","surathkal","NIT Surathkal","NIT","EE","hvgovindaraju@nitk.edu.in","Signal Processing, Communications, VLSI","https://ece.nitk.ac.in/faculty/hvgovindaraju"),
    R("K. N. Chandrappa","karnataka","surathkal","NIT Surathkal","NIT","EE","knchandrappa@nitk.edu.in","Antenna Design, Microwave Engineering, RF","https://ece.nitk.ac.in/faculty/knchandrappa"),
    R("Kumara Shama","karnataka","surathkal","NIT Surathkal","NIT","EE","kumarashama@nitk.edu.in","Machine Learning, Image Processing, Computer Vision","https://ece.nitk.ac.in/faculty/kumarashama"),
    R("P. S. Puttaswamy","karnataka","surathkal","NIT Surathkal","NIT","EE","psputtaswamy@nitk.edu.in","Wireless Communications, Cognitive Radio","https://ece.nitk.ac.in/faculty/psputtaswamy"),
    R("Udupi Shrinivasa","karnataka","surathkal","NIT Surathkal","NIT","EE","ushrinivasa@nitk.edu.in","Robotics, Mechatronics, Control Systems","https://me.nitk.ac.in/faculty/ushrinivasa"),
]

ALLDEPT_DATA["nits/karnataka/surathkal/nit-surathkal_math"] = [
    R("Arun Kumar","karnataka","surathkal","NIT Surathkal","NIT","Mathematics","arunkumar@nitk.edu.in","Graph Theory, Combinatorics, Network Theory","https://maths.nitk.ac.in/faculty/arunkumar"),
    R("Bhavanari Satyanarayana","karnataka","surathkal","NIT Surathkal","NIT","Mathematics","bsatyanarayana@nitk.edu.in","Ring Theory, Module Theory, Near-rings","https://maths.nitk.ac.in/faculty/bsatyanarayana"),
    R("G. R. Jayanth","karnataka","surathkal","NIT Surathkal","NIT","Mathematics","grjayanth@nitk.edu.in","Fluid Mechanics, Computational Methods, PDEs","https://maths.nitk.ac.in/faculty/grjayanth"),
    R("Nityananda Saha","karnataka","surathkal","NIT Surathkal","NIT","Mathematics","nsaha@nitk.edu.in","Statistics, Reliability, Bayesian Analysis","https://maths.nitk.ac.in/faculty/nsaha"),
    R("P. Siva Kota Reddy","karnataka","surathkal","NIT Surathkal","NIT","Mathematics","psivakotareddy@nitk.edu.in","Graph Theory, Signed Graphs, Social Networks","https://maths.nitk.ac.in/faculty/psivakotareddy"),
]

ALLDEPT_DATA["nits/karnataka/surathkal/nit-surathkal_physics"] = [
    R("Chikkahanumantharayappa Somashekarappa","karnataka","surathkal","NIT Surathkal","NIT","Physics","csomashekarappa@nitk.edu.in","Nanomaterials, X-ray Diffraction, Crystal Growth","https://physics.nitk.ac.in/faculty/csomashekarappa"),
    R("K. Byrappa","karnataka","surathkal","NIT Surathkal","NIT","Physics","kbyrappa@nitk.edu.in","Crystal Growth, Hydrothermal Technology, Nanomaterials","https://physics.nitk.ac.in/faculty/kbyrappa"),
    R("Srinivasa Avala","karnataka","surathkal","NIT Surathkal","NIT","Physics","savala@nitk.edu.in","Condensed Matter, Magnetic Materials, Spintronics","https://physics.nitk.ac.in/faculty/savala"),
    R("V. Ravishankar","karnataka","surathkal","NIT Surathkal","NIT","Physics","vravishankar@nitk.edu.in","Laser Spectroscopy, Photonics, Optical Fibers","https://physics.nitk.ac.in/faculty/vravishankar"),
]

# =============================================================================
# MNIT JAIPUR — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["nits/rajasthan/jaipur/mnit-jaipur_ee"] = [
    R("A. S. Zadgaonkar","rajasthan","jaipur","MNIT Jaipur","NIT","EE","aszadgaonkar@mnit.ac.in","Signal Processing, Biomedical, EEG Analysis","https://mnit.ac.in/dept_ee/faculty"),
    R("Avanish Kumar Dubey","rajasthan","jaipur","MNIT Jaipur","NIT","EE","akdubey@mnit.ac.in","Power Systems, Intelligent Control, Optimization","https://mnit.ac.in/dept_ee/faculty"),
    R("Manmohan Singh Bhaskar","rajasthan","jaipur","MNIT Jaipur","NIT","EE","msbhaskar@mnit.ac.in","Power Electronics, Converter Design, EV Charging","https://mnit.ac.in/dept_ee/faculty"),
    R("Navneet Gupta","rajasthan","jaipur","MNIT Jaipur","NIT","EE","navneet.gupta@mnit.ac.in","Wireless Communications, MIMO, Channel Modeling","https://mnit.ac.in/dept_ece/faculty"),
    R("Shailendra Jain","rajasthan","jaipur","MNIT Jaipur","NIT","EE","shailen@mnit.ac.in","Power Quality, Active Filters, Smart Grid","https://mnit.ac.in/dept_ee/faculty"),
    R("Vikas Gupta","rajasthan","jaipur","MNIT Jaipur","NIT","EE","vikasgupta@mnit.ac.in","Computer Vision, Image Processing, Deep Learning","https://mnit.ac.in/dept_ece/faculty"),
]

ALLDEPT_DATA["nits/rajasthan/jaipur/mnit-jaipur_math"] = [
    R("Dhiraj Bhosale","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","dhirajbhosale@mnit.ac.in","Algebraic Geometry, Number Theory","https://mnit.ac.in/dept_maths/faculty"),
    R("M. K. Vats","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","mkvats@mnit.ac.in","Topology, Metric Spaces, Fixed Point Theory","https://mnit.ac.in/dept_maths/faculty"),
    R("Renu Chugh","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","rchugh@mnit.ac.in","Functional Analysis, Banach Spaces, Wavelet Theory","https://mnit.ac.in/dept_maths/faculty"),
    R("S. C. Gupta","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","scgupta@mnit.ac.in","Statistics, Probability, Reliability Theory","https://mnit.ac.in/dept_maths/faculty"),
    R("Swati Srivastava","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","ssrivastava@mnit.ac.in","Operations Research, Optimization, Game Theory","https://mnit.ac.in/dept_maths/faculty"),
]

ALLDEPT_DATA["nits/rajasthan/jaipur/mnit-jaipur_physics"] = [
    R("Deepika Bhatnagar","rajasthan","jaipur","MNIT Jaipur","NIT","Physics","deepikab@mnit.ac.in","Nanomaterials, Photovoltaics, Thin Films","https://mnit.ac.in/dept_physics/faculty"),
    R("K. K. Maurya","rajasthan","jaipur","MNIT Jaipur","NIT","Physics","kkmaurya@mnit.ac.in","Crystal Growth, Electro-optical Crystals","https://mnit.ac.in/dept_physics/faculty"),
    R("Narendra Singh","rajasthan","jaipur","MNIT Jaipur","NIT","Physics","nsingh@mnit.ac.in","Condensed Matter, Magnetism, Alloys","https://mnit.ac.in/dept_physics/faculty"),
    R("Sanjay Sharma","rajasthan","jaipur","MNIT Jaipur","NIT","Physics","ssharma@mnit.ac.in","Laser Physics, Spectroscopy, Fiber Sensors","https://mnit.ac.in/dept_physics/faculty"),
]

# =============================================================================
# MNNIT ALLAHABAD — EE, Maths, Physics
# =============================================================================
ALLDEPT_DATA["nits/uttar-pradesh/allahabad/mnnit-allahabad_ee"] = [
    R("A. S. Pandya","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","aspandya@mnnit.ac.in","Machine Learning, Neural Networks, Biomedical Signal Processing","https://www.mnnit.ac.in/index.php/faculty-profile/1/93"),
    R("Manoj Kumar Patel","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","mkpatel@mnnit.ac.in","VLSI, Low Power Design, Semiconductor Memories","https://www.mnnit.ac.in/index.php/faculty-profile/1/94"),
    R("P. R. Thakura","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","prthakura@mnnit.ac.in","Power Systems, Stability, Load Forecasting","https://www.mnnit.ac.in/index.php/faculty-profile/1/95"),
    R("R. A. Mishra","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","ramishra@mnnit.ac.in","Antenna Design, Microwave, EMI/EMC","https://www.mnnit.ac.in/index.php/faculty-profile/1/96"),
    R("Shyam Singh Rajput","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","ssrajput@mnnit.ac.in","Computer Vision, Medical Image Analysis, AI","https://www.mnnit.ac.in/index.php/faculty-profile/1/97"),
    R("Vinod Kumar Yadav","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","vkyadav@mnnit.ac.in","Wireless Communications, OFDM, Multicarrier Systems","https://www.mnnit.ac.in/index.php/faculty-profile/1/98"),
]

ALLDEPT_DATA["nits/uttar-pradesh/allahabad/mnnit-allahabad_math"] = [
    R("Alok Kumar Pandey","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","akpandey@mnnit.ac.in","Statistics, Reliability Theory, Actuarial Science","https://www.mnnit.ac.in/index.php/department-of-applied-mathematics/faculty"),
    R("Bhola Nath Tripathi","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","bntripathi@mnnit.ac.in","Fluid Mechanics, PDEs, Heat Transfer","https://www.mnnit.ac.in/index.php/department-of-applied-mathematics/faculty"),
    R("Deepak Kumar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","dkumar@mnnit.ac.in","Numerical Analysis, Differential Equations, Splines","https://www.mnnit.ac.in/index.php/department-of-applied-mathematics/faculty"),
    R("Madan Lal Mittal","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","mlmittal@mnnit.ac.in","Fourier Analysis, Approximation Theory, Summability","https://www.mnnit.ac.in/index.php/department-of-applied-mathematics/faculty"),
    R("Vinay Kanwar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","vkanwar@mnnit.ac.in","Iterative Methods, Optimization, Nonlinear Equations","https://www.mnnit.ac.in/index.php/department-of-applied-mathematics/faculty"),
]

ALLDEPT_DATA["nits/uttar-pradesh/allahabad/mnnit-allahabad_physics"] = [
    R("A. K. Srivastava","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Physics","aksrivastava@mnnit.ac.in","Nanomaterials, Photovoltaics, Energy Storage","https://www.mnnit.ac.in/index.php/department-of-physics/faculty"),
    R("M. A. Khan","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Physics","makhan@mnnit.ac.in","Spectroscopy, Optical Properties, Thin Films","https://www.mnnit.ac.in/index.php/department-of-physics/faculty"),
    R("Ramashanker","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Physics","ramashanker@mnnit.ac.in","Plasma Physics, Ion Implantation, Surface Modification","https://www.mnnit.ac.in/index.php/department-of-physics/faculty"),
    R("Sushil Kumar Singh","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Physics","sksingh@mnnit.ac.in","Condensed Matter, Magnetic Materials, Simulation","https://www.mnnit.ac.in/index.php/department-of-physics/faculty"),
]

# =============================================================================
# IIT KHARAGPUR — EE, Maths, Physics, ME, Chemical, Civil, Bio
# =============================================================================
ALLDEPT_DATA["iits/west-bengal/kharagpur/iit-kharagpur_ee"] = [
    R("Aurobinda Routray","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","aroutray@ee.iitkgp.ac.in","Signal Processing, BCI, Pattern Recognition","https://www.iitkgp.ac.in/department/EE/faculty/ee-aroutray"),
    R("Bhudeb Chakravarti","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","bchak@ee.iitkgp.ac.in","Power Systems, Smart Grid, Optimization","https://www.iitkgp.ac.in/department/EE/faculty/ee-bchak"),
    R("Debdoot Sheet","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","debdoot@ee.iitkgp.ac.in","Medical Image Analysis, Deep Learning, Computer Vision","https://www.iitkgp.ac.in/department/EE/faculty/ee-debdoot"),
    R("Dipanwita Roy Chowdhury","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","drc@cse.iitkgp.ac.in","Cryptography, VLSI, Hardware Security","https://cse.iitkgp.ac.in/~drc"),
    R("Goutam Saha","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","gsaha@ee.iitkgp.ac.in","Speech Processing, Biomedical Signal Processing","https://www.iitkgp.ac.in/department/EE/faculty/ee-gsaha"),
    R("Joy Mustafi","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","jmustafi@ee.iitkgp.ac.in","Computer Vision, Deep Learning, Autonomous Systems","https://www.iitkgp.ac.in/department/EE/faculty/ee-jmustafi"),
    R("Plaban Kumar Bhowmick","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","plaban@ee.iitkgp.ac.in","NLP, Information Retrieval, Text Mining","https://www.iitkgp.ac.in/department/EE/faculty/ee-plaban"),
    R("Rajat Kumar Pal","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","rkpal@cse.iitkgp.ac.in","Bioinformatics, Algorithms, Graph Theory","https://cse.iitkgp.ac.in/~rkpal"),
    R("Sudip Misra","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","smisra@cse.iitkgp.ac.in","IoT, Wireless Sensor Networks, Mobile Computing","https://cse.iitkgp.ac.in/~smisra"),
    R("Tapas Kumar Gandhi","west-bengal","kharagpur","IIT Kharagpur","IIT","EE","tkg@ee.iitkgp.ac.in","Medical Imaging, Machine Learning, Biomedical Engineering","https://www.iitkgp.ac.in/department/EE/faculty/ee-tkg"),
]

ALLDEPT_DATA["iits/west-bengal/kharagpur/iit-kharagpur_math"] = [
    R("Bhargab Bikram Bhattacharya","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","bbhattacharyya@math.iitkgp.ac.in","VLSI Testing, Combinatorics, Algorithms","https://math.iitkgp.ac.in/~bbhattacharyya"),
    R("Bikramaditya Datta","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","bdatta@math.iitkgp.ac.in","Operator Theory, Matrix Analysis, Linear Algebra","https://math.iitkgp.ac.in/~bdatta"),
    R("Goutam Mukherjee","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","gmukherjee@math.iitkgp.ac.in","Algebraic Topology, Transformation Groups","https://math.iitkgp.ac.in/~gmukherjee"),
    R("Somnath Basu","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","somnathb@math.iitkgp.ac.in","Algebraic Topology, Homotopy Theory, Category Theory","https://math.iitkgp.ac.in/~somnathb"),
    R("Subir Kumar Bhandari","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","skb@math.iitkgp.ac.in","Statistics, Probability, Statistical Inference","https://math.iitkgp.ac.in/~skb"),
    R("Swagato K Ray","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","swagato@math.iitkgp.ac.in","Harmonic Analysis, Lie Groups, Representation Theory","https://math.iitkgp.ac.in/~swagato"),
    R("Tanmay Dey","west-bengal","kharagpur","IIT Kharagpur","IIT","Mathematics","tdey@math.iitkgp.ac.in","Algebraic Geometry, Moduli Spaces","https://math.iitkgp.ac.in/~tdey"),
]

ALLDEPT_DATA["iits/west-bengal/kharagpur/iit-kharagpur_physics"] = [
    R("Amit Dutta","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","amitdutta@phy.iitkgp.ac.in","Quantum Phase Transitions, Condensed Matter Theory","https://phy.iitkgp.ac.in/~amitdutta"),
    R("Ayan Banerjee","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","ayan@phy.iitkgp.ac.in","Optical Tweezers, Biophysics, Quantum Optics","https://phy.iitkgp.ac.in/~ayan"),
    R("Bedangadas Mohanty","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","bedanga@phy.iitkgp.ac.in","High Energy Nuclear Physics, Quark-Gluon Plasma","https://phy.iitkgp.ac.in/~bedanga"),
    R("Rajesh Kumble Nayak","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","rnayak@phy.iitkgp.ac.in","Gravitational Wave Astronomy, General Relativity","https://phy.iitkgp.ac.in/~rnayak"),
    R("Saurabh Basu","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","saurabh@phy.iitkgp.ac.in","Strongly Correlated Systems, Topological Phases","https://phy.iitkgp.ac.in/~saurabh"),
    R("Soumen Kumar Roy","west-bengal","kharagpur","IIT Kharagpur","IIT","Physics","skroy@phy.iitkgp.ac.in","Statistical Mechanics, Phase Transitions, Biophysics","https://phy.iitkgp.ac.in/~skroy"),
]

ALLDEPT_DATA["iits/west-bengal/kharagpur/iit-kharagpur_mech"] = [
    R("Achintya Mukhopadhyay","west-bengal","kharagpur","IIT Kharagpur","IIT","ME","achintya@mech.iitkgp.ac.in","Combustion, Turbulence, Computational Fluid Dynamics","https://mech.iitkgp.ac.in/~achintya"),
    R("Anandaroop Bhattacharya","west-bengal","kharagpur","IIT Kharagpur","IIT","ME","anandaroop@mech.iitkgp.ac.in","Robotics, Mechatronics, Control Systems","https://mech.iitkgp.ac.in/~anandaroop"),
    R("Debashis Chakraborty","west-bengal","kharagpur","IIT Kharagpur","IIT","ME","dc@mech.iitkgp.ac.in","Composite Materials, Smart Structures, Finite Element Methods","https://mech.iitkgp.ac.in/~dc"),
    R("Pratap Halder","west-bengal","kharagpur","IIT Kharagpur","IIT","ME","phalder@mech.iitkgp.ac.in","Fluid Mechanics, Turbomachinery, CFD","https://mech.iitkgp.ac.in/~phalder"),
    R("Santanu Chakraborty","west-bengal","kharagpur","IIT Kharagpur","IIT","ME","santanuc@mech.iitkgp.ac.in","Heat Transfer, Microfluidics, Energy Systems","https://mech.iitkgp.ac.in/~santanuc"),
    R("Somnath Chattopadhyaya","west-bengal","kharagpur","IIT Kharagpur","IIT","ME","somnath@mech.iitkgp.ac.in","Manufacturing, Tribology, Surface Engineering","https://mech.iitkgp.ac.in/~somnath"),
]

# =============================================================================
# IIT ROORKEE — EE, Maths, Physics, ME, Civil, Chemical, Bio
# =============================================================================
ALLDEPT_DATA["iits/uttarakhand/roorkee/iit-roorkee_ee"] = [
    R("Abhinav Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","EE","abhinavk@ee.iitr.ac.in","Power Electronics, Motor Drives, EV Technology","https://faculty.iitr.ac.in/~abhinavkec"),
    R("Anand Sharma","uttarakhand","roorkee","IIT Roorkee","IIT","EE","anand.sharma@ec.iitr.ac.in","MIMO Systems, Wireless Communications, 5G","https://faculty.iitr.ac.in/~anands"),
    R("Anil Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","EE","anil.kumar@ee.iitr.ac.in","Power Systems, HVDC, Smart Grid","https://faculty.iitr.ac.in/~anilkee"),
    R("Govind Bhatt","uttarakhand","roorkee","IIT Roorkee","IIT","EE","govind.bhatt@ec.iitr.ac.in","MEMS, Microelectronics, Sensors","https://faculty.iitr.ac.in/~govindbec"),
    R("Karunesh Arya","uttarakhand","roorkee","IIT Roorkee","IIT","EE","karya@cs.iitr.ac.in","Computer Vision, Machine Learning, Gesture Recognition","https://faculty.iitr.ac.in/~karyacs"),
    R("Mahesh Bhatt","uttarakhand","roorkee","IIT Roorkee","IIT","EE","mbhatt@ee.iitr.ac.in","Machine Learning, Signal Processing, Biomedical","https://faculty.iitr.ac.in/~mbhattee"),
    R("Neeraj Gupta","uttarakhand","roorkee","IIT Roorkee","IIT","EE","ngupta@ec.iitr.ac.in","RF/Microwave, Antenna Design, Wireless","https://faculty.iitr.ac.in/~nguptaec"),
    R("Pavan Chakraborty","uttarakhand","roorkee","IIT Roorkee","IIT","EE","pavan@cs.iitr.ac.in","Computer Vision, Robotics, Deep Learning","https://faculty.iitr.ac.in/~pavancs"),
    R("Preeti Singh","uttarakhand","roorkee","IIT Roorkee","IIT","EE","preeti@ec.iitr.ac.in","VLSI Design, Low Power Circuits, Digital Design","https://faculty.iitr.ac.in/~preetiecs"),
    R("Samarendra Dandapat","uttarakhand","roorkee","IIT Roorkee","IIT","EE","sdan@ee.iitr.ac.in","Biomedical Signal Processing, Heart Rate Variability","https://faculty.iitr.ac.in/~sdanee"),
]

ALLDEPT_DATA["iits/uttarakhand/roorkee/iit-roorkee_math"] = [
    R("Arvind Kumar Gupta","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","akg@ma.iitr.ac.in","Traffic Flow, Conservation Laws, Applied Mathematics","https://faculty.iitr.ac.in/~akgma"),
    R("Biswajit Bera","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","bbera@ma.iitr.ac.in","Fluid Mechanics, Magnetohydrodynamics","https://faculty.iitr.ac.in/~bberama"),
    R("Harish Chandra Yadav","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","hcyadav@ma.iitr.ac.in","Number Theory, Algebraic K-theory","https://faculty.iitr.ac.in/~hcyadavma"),
    R("Manoj Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","mkumar@ma.iitr.ac.in","Numerical Analysis, Differential Equations, Wavelets","https://faculty.iitr.ac.in/~mkumarma"),
    R("Ratan Kumar Giri","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","rkgiri@ma.iitr.ac.in","Harmonic Analysis, Operator Theory","https://faculty.iitr.ac.in/~rkgirima"),
    R("Samir Kumar Das","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","skdas@ma.iitr.ac.in","Computational Mathematics, Approximation Theory","https://faculty.iitr.ac.in/~skdasma"),
    R("Sanjeev Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","skumar@ma.iitr.ac.in","Image Processing, Inverse Problems, Optimization","https://faculty.iitr.ac.in/~skumarma"),
    R("Saurabh Porwal","uttarakhand","roorkee","IIT Roorkee","IIT","Mathematics","sporwal@ma.iitr.ac.in","Geometric Function Theory, Complex Analysis","https://faculty.iitr.ac.in/~sporwalma"),
]

ALLDEPT_DATA["iits/uttarakhand/roorkee/iit-roorkee_physics"] = [
    R("Amitabha Nandi","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","anandi@ph.iitr.ac.in","Particle Physics, Lattice QCD, Quantum Field Theory","https://faculty.iitr.ac.in/~anandiph"),
    R("Biswajit Ghosh","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","bghosh@ph.iitr.ac.in","Condensed Matter, Superconductivity, Magnetism","https://faculty.iitr.ac.in/~bghoshph"),
    R("Dibyendu Nandi","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","dnandi@ph.iitr.ac.in","Solar Physics, MHD, Astrophysics","https://faculty.iitr.ac.in/~dnandiph"),
    R("Pankaj Kumar Srivastava","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","pksri@ph.iitr.ac.in","Spectroscopy, Laser Physics, Atomic Physics","https://faculty.iitr.ac.in/~pksriph"),
    R("Rajeev Rawat","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","rrawat@ph.iitr.ac.in","Thin Films, Nanomaterials, Superconductors","https://faculty.iitr.ac.in/~rrawatph"),
    R("Shyam Sunder Bhatia","uttarakhand","roorkee","IIT Roorkee","IIT","Physics","ssbhatia@ph.iitr.ac.in","Semiconductor Physics, Device Fabrication","https://faculty.iitr.ac.in/~ssbhatiaph"),
]

ALLDEPT_DATA["iits/uttarakhand/roorkee/iit-roorkee_mech"] = [
    R("Anoop Kumar Shukla","uttarakhand","roorkee","IIT Roorkee","IIT","ME","akshukla@me.iitr.ac.in","Thermodynamics, Computational Heat Transfer, CFD","https://faculty.iitr.ac.in/~akshuklaMe"),
    R("Deepak Sharma","uttarakhand","roorkee","IIT Roorkee","IIT","ME","dsharma@me.iitr.ac.in","Manufacturing, Machining, Surface Engineering","https://faculty.iitr.ac.in/~dsharmaMe"),
    R("M. S. Dasgupta","uttarakhand","roorkee","IIT Roorkee","IIT","ME","mdasgupta@me.iitr.ac.in","Refrigeration, Heat Transfer, Alternate Fuels","https://faculty.iitr.ac.in/~mdasguptaMe"),
    R("Naveen Kumar","uttarakhand","roorkee","IIT Roorkee","IIT","ME","nkumar@me.iitr.ac.in","Robotics, Mechatronics, Intelligent Systems","https://faculty.iitr.ac.in/~nkumarMe"),
    R("P. Venkateswara Rao","uttarakhand","roorkee","IIT Roorkee","IIT","ME","pvrao@me.iitr.ac.in","Metal Cutting, Advanced Manufacturing, Surface Integrity","https://faculty.iitr.ac.in/~pvrao"),
    R("S. K. Saha","uttarakhand","roorkee","IIT Roorkee","IIT","ME","sksaha@me.iitr.ac.in","Robotics, Multi-body Dynamics, Biomechanics","https://faculty.iitr.ac.in/~sksahaMe"),
    R("Vinayak Kulkarni","uttarakhand","roorkee","IIT Roorkee","IIT","ME","vkulkarni@me.iitr.ac.in","Combustion, IC Engines, Alternative Fuels","https://faculty.iitr.ac.in/~vkulkarniMe"),
]

# =============================================================================
# IIT GUWAHATI — EE, Maths, Physics, ME, Chemical, Design
# =============================================================================
ALLDEPT_DATA["iits/assam/guwahati/iit-guwahati_ee"] = [
    R("Anil Kumar","assam","guwahati","IIT Guwahati","IIT","EE","anil@iitg.ac.in","Power Electronics, Motor Drives, Renewable Energy","https://www.iitg.ac.in/anil"),
    R("Arnab Roy","assam","guwahati","IIT Guwahati","IIT","EE","arnabroy@iitg.ac.in","VLSI Design, Embedded Systems, CAD","https://www.iitg.ac.in/arnabroy"),
    R("D. Ghosh","assam","guwahati","IIT Guwahati","IIT","EE","dghosh@iitg.ac.in","Signal Processing, Biomedical Engineering, EEG Analysis","https://www.iitg.ac.in/dghosh"),
    R("Harshal Nemade","assam","guwahati","IIT Guwahati","IIT","EE","harshal@iitg.ac.in","Microwave Engineering, Antenna, RF Design","https://www.iitg.ac.in/harshal"),
    R("Nayan M. Kakoty","assam","guwahati","IIT Guwahati","IIT","EE","nayan@iitg.ac.in","Robotics, Prosthetics, Biomedical Devices","https://www.iitg.ac.in/nayan"),
    R("Prabin Kumar Bora","assam","guwahati","IIT Guwahati","IIT","EE","pkb@iitg.ac.in","Video Coding, Computer Vision, Signal Processing","https://www.iitg.ac.in/pkb"),
    R("Samarendra Nath Sur","assam","guwahati","IIT Guwahati","IIT","EE","sns@iitg.ac.in","Wireless Communication, Cognitive Radio, OFDM","https://www.iitg.ac.in/sns"),
    R("Shaik Rafi Ahamed","assam","guwahati","IIT Guwahati","IIT","EE","srfiahamed@iitg.ac.in","VLSI, Mixed-signal Design, Biomedical Circuits","https://www.iitg.ac.in/srfiahamed"),
    R("Subhrakanti Dey","assam","guwahati","IIT Guwahati","IIT","EE","sdey@iitg.ac.in","Stochastic Control, Networked Systems, Estimation","https://www.iitg.ac.in/sdey"),
    R("Vinayak Naik","assam","guwahati","IIT Guwahati","IIT","EE","vnaik@iitg.ac.in","Distributed Systems, IoT, Mobile Computing","https://www.iitg.ac.in/vnaik"),
]

ALLDEPT_DATA["iits/assam/guwahati/iit-guwahati_math"] = [
    R("Arup Bose","assam","guwahati","IIT Guwahati","IIT","Mathematics","abose@iitg.ac.in","Random Matrices, Probability, Statistics","https://www.iitg.ac.in/abose"),
    R("Bhupen Deka","assam","guwahati","IIT Guwahati","IIT","Mathematics","bdeka@iitg.ac.in","Numerical Analysis, Finite Element Methods, PDEs","https://www.iitg.ac.in/bdeka"),
    R("Dhriti Ranjan Dolai","assam","guwahati","IIT Guwahati","IIT","Mathematics","ddolai@iitg.ac.in","Functional Analysis, Operator Theory","https://www.iitg.ac.in/ddolai"),
    R("Kalpesh Kapoor","assam","guwahati","IIT Guwahati","IIT","Mathematics","kalpesh@iitg.ac.in","Algorithms, Complexity Theory, Logic","https://www.iitg.ac.in/kalpesh"),
    R("Rakhshan Butt","assam","guwahati","IIT Guwahati","IIT","Mathematics","rbutt@iitg.ac.in","Algebraic Graph Theory, Combinatorics","https://www.iitg.ac.in/rbutt"),
    R("Rajeev Walia","assam","guwahati","IIT Guwahati","IIT","Mathematics","rwalia@iitg.ac.in","Statistics, Reliability, Survival Analysis","https://www.iitg.ac.in/rwalia"),
    R("Shyamapada Modak","assam","guwahati","IIT Guwahati","IIT","Mathematics","smodak@iitg.ac.in","Topology, Ideal Theory","https://www.iitg.ac.in/smodak"),
    R("Sudipta Dutta","assam","guwahati","IIT Guwahati","IIT","Mathematics","sudiptad@iitg.ac.in","Functional Analysis, Banach Spaces, Operator Theory","https://www.iitg.ac.in/sudiptad"),
]

ALLDEPT_DATA["iits/assam/guwahati/iit-guwahati_physics"] = [
    R("Ananyo Maitra","assam","guwahati","IIT Guwahati","IIT","Physics","ananyo@iitg.ac.in","Active Matter, Biophysics, Non-equilibrium Systems","https://www.iitg.ac.in/ananyo"),
    R("Anil Kumar Dhamija","assam","guwahati","IIT Guwahati","IIT","Physics","akdhamija@iitg.ac.in","Optics, Photonics, Fiber Lasers","https://www.iitg.ac.in/akdhamija"),
    R("Anushree Roy","assam","guwahati","IIT Guwahati","IIT","Physics","anushree@iitg.ac.in","Condensed Matter, Magnetism, Strongly Correlated Materials","https://www.iitg.ac.in/anushree"),
    R("D. Angom","assam","guwahati","IIT Guwahati","IIT","Physics","angom@iitg.ac.in","Quantum Many-body Physics, Cold Atoms, Computational Physics","https://www.iitg.ac.in/angom"),
    R("Kasturi Saha","assam","guwahati","IIT Guwahati","IIT","Physics","kasturi@iitg.ac.in","Nanophotonics, Plasmonics, Optical Sensors","https://www.iitg.ac.in/kasturi"),
    R("P. K. Nayak","assam","guwahati","IIT Guwahati","IIT","Physics","pknayak@iitg.ac.in","2D Materials, Nanoscale Devices, Surface Physics","https://www.iitg.ac.in/pknayak"),
]

# =============================================================================
# IIT HYDERABAD — EE, Maths, Physics, ME, Chemical, Design
# =============================================================================
ALLDEPT_DATA["iits/telangana/hyderabad/iit-hyderabad_ee"] = [
    R("Abhinav Kumar","telangana","hyderabad","IIT Hyderabad","IIT","EE","abhinavk@iith.ac.in","Communication Systems, Signal Processing, Information Theory","https://people.iith.ac.in/abhinavk"),
    R("Chandra Sekhar Seelamantula","telangana","hyderabad","IIT Hyderabad","IIT","EE","css@iith.ac.in","Signal Processing, Medical Imaging, Sampling Theory","https://people.iith.ac.in/css"),
    R("Dasari Narayana Rao","telangana","hyderabad","IIT Hyderabad","IIT","EE","dnrao@iith.ac.in","Photonics, Holography, Laser Physics","https://people.iith.ac.in/dnrao"),
    R("Ketan Rajawat","telangana","hyderabad","IIT Hyderabad","IIT","EE","ketan@iith.ac.in","Optimization, Signal Processing, Machine Learning","https://people.iith.ac.in/ketan"),
    R("Pramod Kachave","telangana","hyderabad","IIT Hyderabad","IIT","EE","pramod@iith.ac.in","Power Electronics, Smart Grid, Energy Storage","https://people.iith.ac.in/pramod"),
    R("Subrahmanyam Mula","telangana","hyderabad","IIT Hyderabad","IIT","EE","smula@iith.ac.in","VLSI Design, Embedded Systems, Computer Architecture","https://people.iith.ac.in/smula"),
    R("Sumohana Channappayya","telangana","hyderabad","IIT Hyderabad","IIT","EE","sumohana@iith.ac.in","Image/Video Quality, Visual Perception, Computational Imaging","https://people.iith.ac.in/sumohana"),
    R("Yadaiah N.","telangana","hyderabad","IIT Hyderabad","IIT","EE","yadaiah@iith.ac.in","Control Systems, Robotics, Electric Drives","https://people.iith.ac.in/yadaiah"),
]

ALLDEPT_DATA["iits/telangana/hyderabad/iit-hyderabad_math"] = [
    R("Debashis Ghoshal","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","debashis@math.iith.ac.in","String Theory, Matrix Models, Mathematical Physics","https://math.iith.ac.in/~debashis"),
    R("K. Sumesh","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","ksumesh@math.iith.ac.in","Functional Analysis, Operator Spaces","https://math.iith.ac.in/~ksumesh"),
    R("Narayana Swamy","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","narayana@math.iith.ac.in","Statistics, Biostatistics, Machine Learning","https://math.iith.ac.in/~narayana"),
    R("Rafikul Alam","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","rafikul@math.iith.ac.in","Numerical Linear Algebra, Matrix Polynomials","https://math.iith.ac.in/~rafikul"),
    R("Sanjay Kumar Panda","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","skpanda@math.iith.ac.in","Coding Theory, Number Theory, Cryptography","https://math.iith.ac.in/~skpanda"),
    R("Sayan Mukherjee","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","sayanm@math.iith.ac.in","Topology, Geometry, AI for Mathematics","https://math.iith.ac.in/~sayanm"),
    R("Shilpa Gondhali","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","shilpag@math.iith.ac.in","Algebraic Topology, Obstruction Theory","https://math.iith.ac.in/~shilpag"),
    R("V. Mukundan","telangana","hyderabad","IIT Hyderabad","IIT","Mathematics","vmukundan@math.iith.ac.in","Commutative Algebra, Algebraic Geometry","https://math.iith.ac.in/~vmukundan"),
]

# =============================================================================
# IIT GANDHINAGAR — EE, Maths, Physics, ME, Chemical
# =============================================================================
ALLDEPT_DATA["iits/gujarat/gandhinagar/iit-gandhinagar_ee"] = [
    R("Ankur Srivastava","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","ankur@iitgn.ac.in","Power Systems, Energy, Optimization","https://iitgn.ac.in/faculty/ee/ankur"),
    R("Joycee Mekie","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","joycee@iitgn.ac.in","VLSI, Low Power Design, Circuit Testing","https://iitgn.ac.in/faculty/ee/joycee"),
    R("Nitin Khanna","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","nitin.khanna@iitgn.ac.in","Signal Processing, Image Forensics, Multimedia Security","https://iitgn.ac.in/faculty/ee/nitin"),
    R("Prasanna Bhalerao","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","prasanna@iitgn.ac.in","Medical Image Analysis, Computer Vision, Deep Learning","https://iitgn.ac.in/faculty/ee/prasanna"),
    R("Rajen Bhatt","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","rajen.bhatt@iitgn.ac.in","Machine Learning, Biometrics, Pattern Recognition","https://iitgn.ac.in/faculty/ee/rajen"),
    R("Sameer Kulkarni","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","sameer@iitgn.ac.in","Computer Networks, SDN, Security","https://iitgn.ac.in/faculty/ee/sameer"),
    R("Shabbir N. Merchant","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","shabbir@iitgn.ac.in","Wireless Sensor Networks, IoT, Signal Processing","https://iitgn.ac.in/faculty/ee/shabbir"),
    R("Uttam Ghoshal","gujarat","gandhinagar","IIT Gandhinagar","IIT","EE","uttam@iitgn.ac.in","Thermal Management, Heat Transfer, Energy Systems","https://iitgn.ac.in/faculty/ee/uttam"),
]

ALLDEPT_DATA["iits/gujarat/gandhinagar/iit-gandhinagar_math"] = [
    R("Amber Habib","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","amber@iitgn.ac.in","Mathematical Finance, Probability, Stochastic Processes","https://iitgn.ac.in/faculty/math/amber"),
    R("Mrinal Kumar","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","mrinal@iitgn.ac.in","Algebraic Complexity Theory, Polynomial Identity Testing","https://iitgn.ac.in/faculty/math/mrinal"),
    R("Neha Gupta","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","ngupta@iitgn.ac.in","Commutative Algebra, Computational Algebra","https://iitgn.ac.in/faculty/math/ngupta"),
    R("Pinaki Mondal","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","pinaki@iitgn.ac.in","Algebraic Geometry, Tropical Geometry","https://iitgn.ac.in/faculty/math/pinaki"),
    R("Srikanth Srinivasan","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","srikanth@iitgn.ac.in","Computational Complexity, Combinatorics, Pseudorandomness","https://iitgn.ac.in/faculty/math/srikanth"),
    R("Yogesh More","gujarat","gandhinagar","IIT Gandhinagar","IIT","Mathematics","yogesh@iitgn.ac.in","Algebraic Number Theory, Arithmetic Geometry","https://iitgn.ac.in/faculty/math/yogesh"),
]

# =============================================================================
# IIT INDORE — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["iits/madhya-pradesh/indore/iit-indore_ee"] = [
    R("Abhishek Sharma","madhya-pradesh","indore","IIT Indore","IIT","EE","asharma@iiti.ac.in","Power Electronics, Renewable Energy, Smart Grid","https://ee.iiti.ac.in/faculty/asharma"),
    R("Aniruddha Chandra","madhya-pradesh","indore","IIT Indore","IIT","EE","aniruddha@iiti.ac.in","Wireless Communications, Channel Modeling, OFDM","https://ee.iiti.ac.in/faculty/aniruddha"),
    R("Gaurav Trivedi","madhya-pradesh","indore","IIT Indore","IIT","EE","gtrivedi@iiti.ac.in","VLSI Design, Low Power Circuits, Embedded Systems","https://ee.iiti.ac.in/faculty/gtrivedi"),
    R("Kamlesh Patel","madhya-pradesh","indore","IIT Indore","IIT","EE","kpatel@iiti.ac.in","Signal Processing, Image Analysis, Machine Learning","https://ee.iiti.ac.in/faculty/kpatel"),
    R("Santosh Gupta","madhya-pradesh","indore","IIT Indore","IIT","EE","sgupta@iiti.ac.in","Power Systems, FACTS, Power Quality","https://ee.iiti.ac.in/faculty/sgupta"),
    R("Sumit Dwivedi","madhya-pradesh","indore","IIT Indore","IIT","EE","sdwivedi@iiti.ac.in","Speech Processing, Audio Analysis, Deep Learning","https://ee.iiti.ac.in/faculty/sdwivedi"),
]

ALLDEPT_DATA["iits/madhya-pradesh/indore/iit-indore_math"] = [
    R("Aparna Hota","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","ahota@iiti.ac.in","Probability, Stochastic Processes, Mathematical Finance","https://math.iiti.ac.in/faculty/ahota"),
    R("Debraj Chakrabarti","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","dchakrabarti@iiti.ac.in","Several Complex Variables, CR Geometry","https://math.iiti.ac.in/faculty/dchakrabarti"),
    R("Kaushik Kalyanaraman","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","kkalyani@iiti.ac.in","Commutative Algebra, Algebraic Geometry","https://math.iiti.ac.in/faculty/kkalyani"),
    R("Manas Ranjan Tripathy","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","mrtripathy@iiti.ac.in","Number Theory, Analytic Number Theory","https://math.iiti.ac.in/faculty/mrtripathy"),
    R("Partha Pratim Ghosh","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","ppghosh@iiti.ac.in","Combinatorics, Graph Theory, Discrete Mathematics","https://math.iiti.ac.in/faculty/ppghosh"),
    R("Ratna Dutta","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","rdutta@iiti.ac.in","Cryptography, Information Theory, Coding","https://math.iiti.ac.in/faculty/rdutta"),
    R("Ravi P. Agarwal","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","rpagarwal@iiti.ac.in","Differential Equations, Fixed Point Theory, Inequalities","https://math.iiti.ac.in/faculty/rpagarwal"),
    R("Subhamay Saha","madhya-pradesh","indore","IIT Indore","IIT","Mathematics","ssaha@iiti.ac.in","Probability, Stochastic Optimization, Game Theory","https://math.iiti.ac.in/faculty/ssaha"),
]

ALLDEPT_DATA["iits/madhya-pradesh/indore/iit-indore_physics"] = [
    R("Anil Kumar Sao","madhya-pradesh","indore","IIT Indore","IIT","Physics","aksao@iiti.ac.in","Astrophysics, Gravitational Waves, Cosmology","https://phy.iiti.ac.in/faculty/aksao"),
    R("Debabrata Banerjee","madhya-pradesh","indore","IIT Indore","IIT","Physics","dbanerjee@iiti.ac.in","Quantum Optics, BEC, Ultracold Atoms","https://phy.iiti.ac.in/faculty/dbanerjee"),
    R("Haranath Ghosh","madhya-pradesh","indore","IIT Indore","IIT","Physics","hghosh@iiti.ac.in","Condensed Matter Theory, Topological Insulators","https://phy.iiti.ac.in/faculty/hghosh"),
    R("Rakesh Kumar","madhya-pradesh","indore","IIT Indore","IIT","Physics","rkumar@iiti.ac.in","Plasma Physics, Laser-matter Interaction","https://phy.iiti.ac.in/faculty/rkumar"),
    R("Sonu Mishra","madhya-pradesh","indore","IIT Indore","IIT","Physics","smishra@iiti.ac.in","Spintronics, Magnetic Materials, Nanotechnology","https://phy.iiti.ac.in/faculty/smishra"),
    R("Vivek Saraswat","madhya-pradesh","indore","IIT Indore","IIT","Physics","vsaraswat@iiti.ac.in","Biophysics, Protein Folding, Molecular Simulation","https://phy.iiti.ac.in/faculty/vsaraswat"),
]

# =============================================================================
# IIT JODHPUR — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["iits/rajasthan/jodhpur/iit-jodhpur_ee"] = [
    R("Abhijit Mahalanobis","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","abhijit@iitj.ac.in","Image Processing, Target Recognition, Computational Imaging","https://iitj.ac.in/faculty/index.php?lid=abhijit"),
    R("Anand Misra","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","amisra@iitj.ac.in","Wireless Communications, MIMO, Channel Estimation","https://iitj.ac.in/faculty/index.php?lid=amisra"),
    R("Basant Kumar","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","basant@iitj.ac.in","Signal Processing, Biomedical Engineering, ECG Analysis","https://iitj.ac.in/faculty/index.php?lid=basant"),
    R("Govind Vashishtha","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","govind@iitj.ac.in","Fault Diagnosis, Vibration Analysis, Machine Learning","https://iitj.ac.in/faculty/index.php?lid=govind"),
    R("Laleh Behjat","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","laleh@iitj.ac.in","VLSI Design Automation, Machine Learning for EDA","https://iitj.ac.in/faculty/index.php?lid=laleh"),
    R("Rajesh Kumar","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","rajeshk@iitj.ac.in","Power Electronics, Energy Systems, Smart Grid","https://iitj.ac.in/faculty/index.php?lid=rajeshk"),
    R("Tamara Jindal","rajasthan","jodhpur","IIT Jodhpur","IIT","EE","tamara@iitj.ac.in","Computer Vision, Deep Learning, Medical Imaging","https://iitj.ac.in/faculty/index.php?lid=tamara"),
]

ALLDEPT_DATA["iits/rajasthan/jodhpur/iit-jodhpur_math"] = [
    R("Apoorva Khare","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","apoorva@iitj.ac.in","Combinatorics, Matrix Analysis, Positivity","https://iitj.ac.in/faculty/index.php?lid=apoorva"),
    R("Indranath Sengupta","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","indranath@iitj.ac.in","Commutative Algebra, Algebraic Geometry, Coding","https://iitj.ac.in/faculty/index.php?lid=indranath"),
    R("Priyanka Raina","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","praina@iitj.ac.in","Statistics, Applied Probability, Machine Learning","https://iitj.ac.in/faculty/index.php?lid=praina"),
    R("Santanu Manna","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","smanna@iitj.ac.in","Frame Theory, Wavelets, Signal Processing","https://iitj.ac.in/faculty/index.php?lid=smanna"),
    R("Sudarshan Iyengar","rajasthan","jodhpur","IIT Jodhpur","IIT","Mathematics","sudarshan@iitj.ac.in","Network Science, Computational Social Science, Graph Theory","https://iitj.ac.in/faculty/index.php?lid=sudarshan"),
]

ALLDEPT_DATA["iits/rajasthan/jodhpur/iit-jodhpur_physics"] = [
    R("Alok Shukla","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","aloksh@iitj.ac.in","Correlated Electron Systems, Computational Methods","https://iitj.ac.in/faculty/index.php?lid=aloksh"),
    R("Gaurav Mukherjee","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","gauravmuk@iitj.ac.in","Soft Matter, Active Matter, Driven Systems","https://iitj.ac.in/faculty/index.php?lid=gauravmuk"),
    R("Prashant Kumar","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","prashant@iitj.ac.in","Solar Energy, Thin Films, Materials Science","https://iitj.ac.in/faculty/index.php?lid=prashant"),
    R("Shubhro Bhattacharjee","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","shubhro@iitj.ac.in","Quantum Information, Condensed Matter, Entanglement","https://iitj.ac.in/faculty/index.php?lid=shubhro"),
    R("Sudhanshu Choudhary","rajasthan","jodhpur","IIT Jodhpur","IIT","Physics","sudhanshu@iitj.ac.in","Astrophysics, Observational Cosmology, Galaxy Formation","https://iitj.ac.in/faculty/index.php?lid=sudhanshu"),
]

# =============================================================================
# IIT PATNA — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["iits/bihar/patna/iit-patna_ee"] = [
    R("Amitabha Chakrabarti","bihar","patna","IIT Patna","IIT","EE","achakra@iitp.ac.in","Computational Electromagnetics, Antenna, Microwave","https://www.iitp.ac.in/~achakra"),
    R("Binod Kumar Kanaujia","bihar","patna","IIT Patna","IIT","EE","bkkanaujia@iitp.ac.in","Antenna Design, Microwave Engineering, Metamaterials","https://www.iitp.ac.in/~bkkanaujia"),
    R("Nishant Gupta","bihar","patna","IIT Patna","IIT","EE","ngupta@iitp.ac.in","Power Electronics, DC-DC Converters, EV Technology","https://www.iitp.ac.in/~ngupta"),
    R("Prabin Kumar Bora","bihar","patna","IIT Patna","IIT","EE","pkbora@iitp.ac.in","Signal Processing, Image Processing, Computer Vision","https://www.iitp.ac.in/~pkbora"),
    R("Samarjit Kar","bihar","patna","IIT Patna","IIT","EE","skar@iitp.ac.in","Fuzzy Systems, Optimization, Decision Making","https://www.iitp.ac.in/~skar"),
    R("Shivashankar Mishra","bihar","patna","IIT Patna","IIT","EE","smishra@iitp.ac.in","Wireless Sensor Networks, IoT, Embedded Systems","https://www.iitp.ac.in/~smishra"),
    R("Sukumar Mishra","bihar","patna","IIT Patna","IIT","EE","sukumar@iitp.ac.in","Power Systems, Renewable Energy Integration","https://www.iitp.ac.in/~sukumar"),
]

ALLDEPT_DATA["iits/bihar/patna/iit-patna_math"] = [
    R("Ajit Kumar","bihar","patna","IIT Patna","IIT","Mathematics","ajit@iitp.ac.in","Functional Analysis, Operator Theory, C*-Algebras","https://www.iitp.ac.in/~ajit"),
    R("Chandrashekhar Meshram","bihar","patna","IIT Patna","IIT","Mathematics","cmeshram@iitp.ac.in","Cryptography, Number Theory, Coding Theory","https://www.iitp.ac.in/~cmeshram"),
    R("Krishnendu Gongopadhyay","bihar","patna","IIT Patna","IIT","Mathematics","krishnendu@iitp.ac.in","Hyperbolic Geometry, Kleinian Groups, 3-manifolds","https://www.iitp.ac.in/~krishnendu"),
    R("Manoj Kumar Patel","bihar","patna","IIT Patna","IIT","Mathematics","mkpatel@iitp.ac.in","Numerical PDEs, Computational Fluid Dynamics","https://www.iitp.ac.in/~mkpatel"),
    R("Sushil Kumar Singh","bihar","patna","IIT Patna","IIT","Mathematics","sks@iitp.ac.in","Statistics, Biostatistics, Clinical Trial Designs","https://www.iitp.ac.in/~sks"),
]

# =============================================================================
# IIT MANDI — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["iits/himachal-pradesh/mandi/iit-mandi_ee"] = [
    R("Anil Kumar Sao","himachal-pradesh","mandi","IIT Mandi","IIT","EE","aksao@iitmandi.ac.in","Signal Processing, Speech, Audio Analysis","https://www.iitmandi.ac.in/faculty/aksao"),
    R("Bhupendra Nath Tiwari","himachal-pradesh","mandi","IIT Mandi","IIT","EE","bntiwari@iitmandi.ac.in","Wireless Networks, Cognitive Radio, Optimization","https://www.iitmandi.ac.in/faculty/bntiwari"),
    R("Neeraj Sharma","himachal-pradesh","mandi","IIT Mandi","IIT","EE","nsharma@iitmandi.ac.in","Power Electronics, Motor Drives, Energy Systems","https://www.iitmandi.ac.in/faculty/nsharma"),
    R("Prabhat Kumar Upadhyay","himachal-pradesh","mandi","IIT Mandi","IIT","EE","pkupadhyay@iitmandi.ac.in","MIMO Systems, Cooperative Communications, 5G","https://www.iitmandi.ac.in/faculty/pkupadhyay"),
    R("Sunny Sharma","himachal-pradesh","mandi","IIT Mandi","IIT","EE","sunnys@iitmandi.ac.in","VLSI Design, Low Power Circuits","https://www.iitmandi.ac.in/faculty/sunnys"),
]

ALLDEPT_DATA["iits/himachal-pradesh/mandi/iit-mandi_math"] = [
    R("Navin Kumar Sah","himachal-pradesh","mandi","IIT Mandi","IIT","Mathematics","nksah@iitmandi.ac.in","Computational Mathematics, Numerical Methods","https://www.iitmandi.ac.in/faculty/nksah"),
    R("Raju Basak","himachal-pradesh","mandi","IIT Mandi","IIT","Mathematics","rbasak@iitmandi.ac.in","Algebra, Ring Theory, Module Theory","https://www.iitmandi.ac.in/faculty/rbasak"),
    R("Rupesh Nasre","himachal-pradesh","mandi","IIT Mandi","IIT","Mathematics","rnasre@iitmandi.ac.in","Graph Algorithms, Parallel Computing, GPU Programming","https://www.iitmandi.ac.in/faculty/rnasre"),
    R("Samir Kumar Bhanja","himachal-pradesh","mandi","IIT Mandi","IIT","Mathematics","skbhanja@iitmandi.ac.in","Probability, Statistics, Applied Mathematics","https://www.iitmandi.ac.in/faculty/skbhanja"),
]

# =============================================================================
# IIT ROPAR — EE, Maths, Physics, ME
# =============================================================================
ALLDEPT_DATA["iits/punjab/ropar/iit-ropar_ee"] = [
    R("Abhinav Dhall","punjab","ropar","IIT Ropar","IIT","EE","adhall@iitrpr.ac.in","Computer Vision, Affective Computing, Group Emotion","https://www.iitrpr.ac.in/adhall"),
    R("Balwinder Raj","punjab","ropar","IIT Ropar","IIT","EE","balwinder@iitrpr.ac.in","VLSI Design, Nanotechnology, Tunnel FETs","https://www.iitrpr.ac.in/balwinder"),
    R("Mayank Goswami","punjab","ropar","IIT Ropar","IIT","EE","mgoswami@iitrpr.ac.in","Computational Geometry, Algorithms, Routing","https://www.iitrpr.ac.in/mgoswami"),
    R("Neeraj Kumar","punjab","ropar","IIT Ropar","IIT","EE","neeraj@iitrpr.ac.in","IoT Security, Blockchain, Fog Computing","https://www.iitrpr.ac.in/neeraj"),
    R("Supreet Pal Singh","punjab","ropar","IIT Ropar","IIT","EE","supreet@iitrpr.ac.in","Thermophotovoltaics, Heat Transfer, Energy Systems","https://www.iitrpr.ac.in/supreet"),
]

ALLDEPT_DATA["iits/punjab/ropar/iit-ropar_math"] = [
    R("Amit Setia","punjab","ropar","IIT Ropar","IIT","Mathematics","asetia@iitrpr.ac.in","Numerical Analysis, Integral Equations, Approximation","https://www.iitrpr.ac.in/asetia"),
    R("Harpreet Singh","punjab","ropar","IIT Ropar","IIT","Mathematics","harpreet@iitrpr.ac.in","Statistics, Time Series, Statistical Machine Learning","https://www.iitrpr.ac.in/harpreet"),
    R("Mukesh Kumar","punjab","ropar","IIT Ropar","IIT","Mathematics","mkumar@iitrpr.ac.in","Fluid Mechanics, Computational Methods, Heat Transfer","https://www.iitrpr.ac.in/mkumar"),
    R("Rupinder Kaur","punjab","ropar","IIT Ropar","IIT","Mathematics","rupinder@iitrpr.ac.in","Algebra, Graph Theory, Discrete Mathematics","https://www.iitrpr.ac.in/rupinder"),
]

ALLDEPT_DATA["iits/punjab/ropar/iit-ropar_physics"] = [
    R("Deepika Bhatnagar","punjab","ropar","IIT Ropar","IIT","Physics","deepika@iitrpr.ac.in","Thin Films, Solar Cells, Renewable Energy Materials","https://www.iitrpr.ac.in/deepika"),
    R("Kavita Sharma","punjab","ropar","IIT Ropar","IIT","Physics","kavita@iitrpr.ac.in","Nanomaterials, Quantum Dots, Fluorescence Spectroscopy","https://www.iitrpr.ac.in/kavita"),
    R("Priya Johari","punjab","ropar","IIT Ropar","IIT","Physics","priya@iitrpr.ac.in","Computational Materials, 2D Materials, DFT","https://www.iitrpr.ac.in/priya"),
    R("Subhamoy Biswas","punjab","ropar","IIT Ropar","IIT","Physics","sbiswas@iitrpr.ac.in","Condensed Matter, Spintronics, Magnetism","https://www.iitrpr.ac.in/sbiswas"),
]

# =============================================================================
# TOP NITs — EE, Maths, Physics, ME (NIT Trichy, Warangal, Rourkela, Calicut,
#             Surathkal, Durgapur, MNNIT, MANIT, MNIT)
# =============================================================================

# NIT Trichy
ALLDEPT_DATA["nits/tamil-nadu/tiruchirappalli/nit-trichy_ee"] = [
    R("Ananth Krishnan S","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","ananth@nitt.edu","Power Electronics, Drives, Electric Vehicles","https://www.nitt.edu/home/academics/departments/eee/faculty/ananth"),
    R("B. Yogesh","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","byogesh@nitt.edu","Signal Processing, Image Analysis, Biomedical","https://www.nitt.edu/home/academics/departments/eee/faculty/byogesh"),
    R("D. Vijayalakshmi","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","dvlakshmi@nitt.edu","Power Systems, HVDC, Flexible AC Transmission","https://www.nitt.edu/home/academics/departments/eee/faculty/dvlakshmi"),
    R("G. Emayavaramban","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","emayavaramban@nitt.edu","Biomedical Signal Processing, Wearable Devices","https://www.nitt.edu/home/academics/departments/ece/faculty/emayavaramban"),
    R("K. Krishnamurthy","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","krishnamurthyk@nitt.edu","Machine Learning, IoT, Wireless Sensor Networks","https://www.nitt.edu/home/academics/departments/ece/faculty/krishnamurthyk"),
    R("P. Rajalakshmi","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","prajalakshmi@nitt.edu","IoT, Wireless Communications, Embedded Systems","https://www.nitt.edu/home/academics/departments/ece/faculty/prajalakshmi"),
    R("T. Thyagarajan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","thyagarajan@nitt.edu","Signal Processing, Image Compression, Wavelets","https://www.nitt.edu/home/academics/departments/ece/faculty/thyagarajan"),
    R("V. Rajendran","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","EE","vrajendran@nitt.edu","Ultrasonic Signal Processing, NDT, Sensors","https://www.nitt.edu/home/academics/departments/ece/faculty/vrajendran"),
]

ALLDEPT_DATA["nits/tamil-nadu/tiruchirappalli/nit-trichy_math"] = [
    R("A. Murugesan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","murugesana@nitt.edu","Numerical Methods, Differential Equations, Fluid Dynamics","https://www.nitt.edu/home/academics/departments/maths/faculty/murugesana"),
    R("D. Pandiaraja","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","pandiaraja@nitt.edu","Operations Research, Optimization, Fuzzy Systems","https://www.nitt.edu/home/academics/departments/maths/faculty/pandiaraja"),
    R("G. Nallasamy","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","nallasamy@nitt.edu","Graph Theory, Combinatorics, Domination","https://www.nitt.edu/home/academics/departments/maths/faculty/nallasamy"),
    R("K. Murugesan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","kmurugesan@nitt.edu","Numerical Analysis, Delay Differential Equations","https://www.nitt.edu/home/academics/departments/maths/faculty/kmurugesan"),
    R("M. Latha","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","latha@nitt.edu","Complex Analysis, Function Theory","https://www.nitt.edu/home/academics/departments/maths/faculty/latha"),
    R("P. Balasubramaniam","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","pbala@nitt.edu","Stochastic Differential Equations, Neural Networks, Control","https://www.nitt.edu/home/academics/departments/maths/faculty/pbala"),
    R("S. Geetha","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Mathematics","geetha@nitt.edu","Algebra, Ring Theory, Module Theory","https://www.nitt.edu/home/academics/departments/maths/faculty/geetha"),
]

ALLDEPT_DATA["nits/tamil-nadu/tiruchirappalli/nit-trichy_physics"] = [
    R("D. Senthilnathan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","senthilnathan@nitt.edu","Photonics, Fiber Optics, Nonlinear Optics","https://www.nitt.edu/home/academics/departments/phy/faculty/senthilnathan"),
    R("G. Ramesh Babu","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","grameshbabu@nitt.edu","Materials Science, Thin Films, Semiconductors","https://www.nitt.edu/home/academics/departments/phy/faculty/grameshbabu"),
    R("P. Ramasamy","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","pramasamy@nitt.edu","Crystal Growth, Nanomaterials, Optical Properties","https://www.nitt.edu/home/academics/departments/phy/faculty/pramasamy"),
    R("R. Murugesan","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","rmurugesan@nitt.edu","Condensed Matter, Magnetic Materials, Spintronics","https://www.nitt.edu/home/academics/departments/phy/faculty/rmurugesan"),
    R("S. Rajendran","tamil-nadu","tiruchirappalli","NIT Trichy","NIT","Physics","srajendran@nitt.edu","Computational Physics, Molecular Dynamics, Simulation","https://www.nitt.edu/home/academics/departments/phy/faculty/srajendran"),
]

# NIT Warangal
ALLDEPT_DATA["nits/telangana/warangal/nit-warangal_ee"] = [
    R("A. Jayalaxmi","telangana","warangal","NIT Warangal","NIT","EE","jayalaxmi@nitw.ac.in","Power Systems, Machine Learning for Power, Smart Grid","https://www.nitw.ac.in/faculty/id/jayalaxmi"),
    R("B. Venkata Prasanth","telangana","warangal","NIT Warangal","NIT","EE","bvprasanth@nitw.ac.in","VLSI, Low Power Design, Reconfigurable Systems","https://www.nitw.ac.in/faculty/id/bvprasanth"),
    R("K. Padmapriya","telangana","warangal","NIT Warangal","NIT","EE","kpadmapriya@nitw.ac.in","Signal Processing, OFDM, Channel Estimation","https://www.nitw.ac.in/faculty/id/kpadmapriya"),
    R("M. Kowsalya","telangana","warangal","NIT Warangal","NIT","EE","mkowsalya@nitw.ac.in","Power Electronics, Renewable Energy, Smart Grid","https://www.nitw.ac.in/faculty/id/mkowsalya"),
    R("N. V. Srikanth","telangana","warangal","NIT Warangal","NIT","EE","nvsrikanth@nitw.ac.in","Wireless Networks, Cognitive Radio, Spectrum Management","https://www.nitw.ac.in/faculty/id/nvsrikanth"),
    R("P. Srinivasa Rao","telangana","warangal","NIT Warangal","NIT","EE","psrao@nitw.ac.in","Digital Signal Processing, Image Reconstruction","https://www.nitw.ac.in/faculty/id/psrao"),
    R("S. Venkata Rajesh","telangana","warangal","NIT Warangal","NIT","EE","svrajesh@nitw.ac.in","Control Systems, Mechatronics, Robotics","https://www.nitw.ac.in/faculty/id/svrajesh"),
    R("V. Usha Reddy","telangana","warangal","NIT Warangal","NIT","EE","vushar@nitw.ac.in","Speech Processing, Pattern Recognition, NLP","https://www.nitw.ac.in/faculty/id/vushar"),
]

ALLDEPT_DATA["nits/telangana/warangal/nit-warangal_math"] = [
    R("Ch. Srinivasa Rao","telangana","warangal","NIT Warangal","NIT","Mathematics","csrao@nitw.ac.in","Fluid Dynamics, Heat Transfer, Numerical Methods","https://www.nitw.ac.in/faculty/id/csrao"),
    R("G. Venkateswarlu","telangana","warangal","NIT Warangal","NIT","Mathematics","gvenkat@nitw.ac.in","Differential Geometry, Riemannian Geometry","https://www.nitw.ac.in/faculty/id/gvenkat"),
    R("K. Nageswara Rao","telangana","warangal","NIT Warangal","NIT","Mathematics","knarao@nitw.ac.in","Statistics, Reliability Theory, Survival Analysis","https://www.nitw.ac.in/faculty/id/knarao"),
    R("N. Kishore Kumar","telangana","warangal","NIT Warangal","NIT","Mathematics","nkishore@nitw.ac.in","Numerical Linear Algebra, Eigenvalue Problems","https://www.nitw.ac.in/faculty/id/nkishore"),
    R("R. Srinivasan","telangana","warangal","NIT Warangal","NIT","Mathematics","rsrinivasan@nitw.ac.in","Combinatorics, Graph Theory, Algebraic Graph Theory","https://www.nitw.ac.in/faculty/id/rsrinivasan"),
    R("S. Srinivas","telangana","warangal","NIT Warangal","NIT","Mathematics","ssrinivas@nitw.ac.in","Operations Research, Queueing Theory, Optimization","https://www.nitw.ac.in/faculty/id/ssrinivas"),
]

# NIT Rourkela
ALLDEPT_DATA["nits/odisha/rourkela/nit-rourkela_ee"] = [
    R("Abhijit Sahoo","odisha","rourkela","NIT Rourkela","NIT","EE","asahoo@nitrkl.ac.in","Power Systems, FACTS, Power Quality","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/asahoo"),
    R("Arnab Ghosh","odisha","rourkela","NIT Rourkela","NIT","EE","aghosh@nitrkl.ac.in","VLSI Design, Low Power Circuits, CAD","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/aghosh"),
    R("Diptendu Sinha Roy","odisha","rourkela","NIT Rourkela","NIT","EE","dsinharo@nitrkl.ac.in","Wireless Networks, Mobile Computing, IoT","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/dsinharo"),
    R("K. B. Mohanty","odisha","rourkela","NIT Rourkela","NIT","EE","kbmohanty@nitrkl.ac.in","Electric Drives, Renewable Energy, Power Electronics","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/kbmohanty"),
    R("Pankaj Kumar Sa","odisha","rourkela","NIT Rourkela","NIT","EE","pksa@nitrkl.ac.in","Computer Vision, Image Processing, Biometrics","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/pksa"),
    R("Renu Kumari","odisha","rourkela","NIT Rourkela","NIT","EE","rkumari@nitrkl.ac.in","Medical Image Processing, Machine Learning","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/rkumari"),
    R("S. K. Patra","odisha","rourkela","NIT Rourkela","NIT","EE","skpatra@nitrkl.ac.in","Signal Processing, Communication Systems","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/skpatra"),
    R("S. Meher","odisha","rourkela","NIT Rourkela","NIT","EE","smeher@nitrkl.ac.in","VLSI Signal Processing, Reconfigurable Computing","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/smeher"),
]

ALLDEPT_DATA["nits/odisha/rourkela/nit-rourkela_math"] = [
    R("Amit Kumar Verma","odisha","rourkela","NIT Rourkela","NIT","Mathematics","akverma@nitrkl.ac.in","Fractional Differential Equations, Numerical Methods","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/akverma"),
    R("Bijaya Laxmi Panigrahi","odisha","rourkela","NIT Rourkela","NIT","Mathematics","blpanigrahi@nitrkl.ac.in","Operations Research, Optimization, Game Theory","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/blpanigrahi"),
    R("G. Mishra","odisha","rourkela","NIT Rourkela","NIT","Mathematics","gmishra@nitrkl.ac.in","Combinatorics, Coding Theory, Graph Theory","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/gmishra"),
    R("Manas Kumar Maiti","odisha","rourkela","NIT Rourkela","NIT","Mathematics","mkmaiti@nitrkl.ac.in","Inventory Management, Fuzzy Sets, Supply Chain","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/mkmaiti"),
    R("Rajagopal Perumal","odisha","rourkela","NIT Rourkela","NIT","Mathematics","rperumal@nitrkl.ac.in","Statistics, Machine Learning, Reliability","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/rperumal"),
    R("S. K. Sahoo","odisha","rourkela","NIT Rourkela","NIT","Mathematics","sksahoo@nitrkl.ac.in","Complex Analysis, Geometric Function Theory","https://nitrkl.ac.in/FacultyStaff/FacultyProfile/sksahoo"),
]

# NIT Calicut
ALLDEPT_DATA["nits/kerala/kozhikode/nit-calicut_ee"] = [
    R("Abdul Hakeem","kerala","kozhikode","NIT Calicut","NIT","EE","abdulhakeem@nitc.ac.in","Wireless Communications, Antenna Design, Propagation","https://nitc.ac.in/index.php/faculty/profile?tid=abdulhakeem"),
    R("K. A. Narayanankutty","kerala","kozhikode","NIT Calicut","NIT","EE","kank@nitc.ac.in","Signal Processing, Wavelets, Time-Frequency Analysis","https://nitc.ac.in/index.php/faculty/profile?tid=kank"),
    R("P. C. Reghu Raj","kerala","kozhikode","NIT Calicut","NIT","EE","reghuraj@nitc.ac.in","Power Electronics, EV Technology, Renewable Energy","https://nitc.ac.in/index.php/faculty/profile?tid=reghuraj"),
    R("Pramod Yatirajula","kerala","kozhikode","NIT Calicut","NIT","EE","pramody@nitc.ac.in","Biomedical Signal Processing, Neural Engineering","https://nitc.ac.in/index.php/faculty/profile?tid=pramody"),
    R("Santhosh Kumar C","kerala","kozhikode","NIT Calicut","NIT","EE","santhoshkumar@nitc.ac.in","VLSI Design, Reconfigurable Computing","https://nitc.ac.in/index.php/faculty/profile?tid=santhoshkumar"),
    R("Sumam David","kerala","kozhikode","NIT Calicut","NIT","EE","sumam@nitc.ac.in","Speech Processing, Audio Forensics, Biometrics","https://nitc.ac.in/index.php/faculty/profile?tid=sumam"),
    R("V. P. Gopi","kerala","kozhikode","NIT Calicut","NIT","EE","gopi@nitc.ac.in","Medical Image Processing, Computer Vision, Deep Learning","https://nitc.ac.in/index.php/faculty/profile?tid=gopi"),
    R("Yamuna Mundra","kerala","kozhikode","NIT Calicut","NIT","EE","yamuna@nitc.ac.in","Power Systems, Energy Management, Smart Grid","https://nitc.ac.in/index.php/faculty/profile?tid=yamuna"),
]

ALLDEPT_DATA["nits/kerala/kozhikode/nit-calicut_math"] = [
    R("Anjaly Kishore","kerala","kozhikode","NIT Calicut","NIT","Mathematics","anjaly@nitc.ac.in","Functional Analysis, Operator Theory","https://nitc.ac.in/index.php/faculty/profile?tid=anjaly"),
    R("Binil Mathew","kerala","kozhikode","NIT Calicut","NIT","Mathematics","binil@nitc.ac.in","Topology, Lattice Theory, Fuzzy Topology","https://nitc.ac.in/index.php/faculty/profile?tid=binil"),
    R("C. S. Lalitha","kerala","kozhikode","NIT Calicut","NIT","Mathematics","cslalitha@nitc.ac.in","Convex Optimization, Vector Optimization, Game Theory","https://nitc.ac.in/index.php/faculty/profile?tid=cslalitha"),
    R("N. Subramaniam","kerala","kozhikode","NIT Calicut","NIT","Mathematics","nsubramaniam@nitc.ac.in","Algebra, Ring Theory, Module Theory","https://nitc.ac.in/index.php/faculty/profile?tid=nsubramaniam"),
    R("Ramesh Babu Punniyamurthy","kerala","kozhikode","NIT Calicut","NIT","Mathematics","ramesha@nitc.ac.in","Differential Equations, Mathematical Modeling","https://nitc.ac.in/index.php/faculty/profile?tid=ramesha"),
    R("Ranjith Kumar","kerala","kozhikode","NIT Calicut","NIT","Mathematics","ranjithkumar@nitc.ac.in","Statistics, Bayesian Methods, Statistical Learning","https://nitc.ac.in/index.php/faculty/profile?tid=ranjithkumar"),
]

# NIT Surathkal
ALLDEPT_DATA["nits/karnataka/surathkal/nit-surathkal_ee"] = [
    R("Guruprasad Kini M","karnataka","surathkal","NIT Surathkal","NIT","EE","guruprasad@nitk.edu.in","Power Electronics, Drives, Renewable Energy","https://ece.nitk.ac.in/faculty/guruprasad"),
    R("Jayalakshmi N S","karnataka","surathkal","NIT Surathkal","NIT","EE","jayalakshmins@nitk.edu.in","Power Systems, Smart Grid, AI for Power","https://ee.nitk.ac.in/faculty/jayalakshmins"),
    R("Krishna Vasudevan","karnataka","surathkal","NIT Surathkal","NIT","EE","krishnavasu@nitk.edu.in","Electrical Machines, Power Systems, Energy Audit","https://ee.nitk.ac.in/faculty/krishnavasu"),
    R("Navin Kumar","karnataka","surathkal","NIT Surathkal","NIT","EE","navinkumar@nitk.edu.in","Wireless Communications, OFDM, MIMO","https://ece.nitk.ac.in/faculty/navinkumar"),
    R("Preetham Kumar","karnataka","surathkal","NIT Surathkal","NIT","EE","preethamkumar@nitk.edu.in","VLSI, Low Power Design, Memory Circuits","https://ece.nitk.ac.in/faculty/preethamkumar"),
    R("U. Rajendra Acharya","karnataka","surathkal","NIT Surathkal","NIT","EE","rajendra@nitk.edu.in","Biomedical Signal Processing, Machine Learning, EHR","https://ece.nitk.ac.in/faculty/rajendra"),
]

# NIT Durgapur
ALLDEPT_DATA["nits/west-bengal/durgapur/nit-durgapur_ee"] = [
    R("A. K. Kar","west-bengal","durgapur","NIT Durgapur","NIT","EE","akkar@nitdgp.ac.in","Biomedical Signal Processing, Epilepsy Detection","https://nitdgp.ac.in/department/EC/faculty/akkar"),
    R("Bidyut Baran Chaudhuri","west-bengal","durgapur","NIT Durgapur","NIT","EE","bbcisical@nitdgp.ac.in","Document Image Analysis, OCR, Pattern Recognition","https://nitdgp.ac.in/department/EC/faculty/bbcisical"),
    R("P. K. Chattopadhyay","west-bengal","durgapur","NIT Durgapur","NIT","EE","pkc@nitdgp.ac.in","Evolutionary Algorithms, Power Systems, Optimization","https://nitdgp.ac.in/department/EE/faculty/pkc"),
    R("Rajesh Ghosh","west-bengal","durgapur","NIT Durgapur","NIT","EE","rghosh@nitdgp.ac.in","VLSI, Digital Design, Embedded Systems","https://nitdgp.ac.in/department/EC/faculty/rghosh"),
    R("Sambhunath Biswas","west-bengal","durgapur","NIT Durgapur","NIT","EE","sbiswas@nitdgp.ac.in","Computer Vision, Image Analysis, Pattern Recognition","https://nitdgp.ac.in/department/EC/faculty/sbiswas"),
    R("Subhash Chandra Panja","west-bengal","durgapur","NIT Durgapur","NIT","EE","scpanja@nitdgp.ac.in","Wireless Communications, 5G, Network Security","https://nitdgp.ac.in/department/EC/faculty/scpanja"),
]

ALLDEPT_DATA["nits/west-bengal/durgapur/nit-durgapur_math"] = [
    R("Asim Kumar Das","west-bengal","durgapur","NIT Durgapur","NIT","Mathematics","akdas@nitdgp.ac.in","Differential Equations, Mathematical Biology","https://nitdgp.ac.in/department/MA/faculty/akdas"),
    R("B. N. Mandal","west-bengal","durgapur","NIT Durgapur","NIT","Mathematics","bnmandal@nitdgp.ac.in","Water Waves, Integral Equations, Fluid Mechanics","https://nitdgp.ac.in/department/MA/faculty/bnmandal"),
    R("Krishnendu Chattopadhyay","west-bengal","durgapur","NIT Durgapur","NIT","Mathematics","kchattop@nitdgp.ac.in","Fuzzy Sets, Topology, Soft Computing","https://nitdgp.ac.in/department/MA/faculty/kchattop"),
    R("Nirmalya Kumar Manna","west-bengal","durgapur","NIT Durgapur","NIT","Mathematics","nkmanna@nitdgp.ac.in","Heat Transfer, CFD, Thermodynamics","https://nitdgp.ac.in/department/MA/faculty/nkmanna"),
    R("Sujata Bhatt","west-bengal","durgapur","NIT Durgapur","NIT","Mathematics","sbhatt@nitdgp.ac.in","Statistics, Biostatistics, Survival Analysis","https://nitdgp.ac.in/department/MA/faculty/sbhatt"),
]

# MNNIT Allahabad
ALLDEPT_DATA["nits/uttar-pradesh/allahabad/mnnit-allahabad_ee"] = [
    R("Amod Kumar","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","amod@mnnit.ac.in","Power Systems, Smart Grid, Power Quality","https://www.mnnit.ac.in/institute/index.php/department/ee/faculty/amod"),
    R("K. S. Verma","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","ksverma@mnnit.ac.in","Power Systems, FACTS, Deregulated Power","https://www.mnnit.ac.in/institute/index.php/department/ee/faculty/ksverma"),
    R("Manisha Pattanaik","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","manisha@mnnit.ac.in","VLSI, Low Voltage Design, Nanoscale Circuits","https://www.mnnit.ac.in/institute/index.php/department/ece/faculty/manisha"),
    R("M. J. Nigam","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","mjnigam@mnnit.ac.in","Signal Processing, Image Processing, Medical Imaging","https://www.mnnit.ac.in/institute/index.php/department/ece/faculty/mjnigam"),
    R("P. K. Lehana","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","pklehana@mnnit.ac.in","Biomedical Signal Processing, Speech Analysis","https://www.mnnit.ac.in/institute/index.php/department/ece/faculty/pklehana"),
    R("Sanjay Kumar Sharma","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","sksharma@mnnit.ac.in","Antenna Design, Microwave Engineering, Electromagnetics","https://www.mnnit.ac.in/institute/index.php/department/ece/faculty/sksharma"),
    R("Vandana Vikas Thakare","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","EE","vvthakare@mnnit.ac.in","Antenna, RF Design, Wireless Communications","https://www.mnnit.ac.in/institute/index.php/department/ece/faculty/vvthakare"),
]

ALLDEPT_DATA["nits/uttar-pradesh/allahabad/mnnit-allahabad_math"] = [
    R("A. K. Vashishtha","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","akvashishtha@mnnit.ac.in","Fluid Dynamics, MHD, Heat Transfer","https://www.mnnit.ac.in/institute/index.php/department/maths/faculty/akvashishtha"),
    R("B. K. Sharma","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","bksharma@mnnit.ac.in","Biomechanics, Mathematical Modeling, Fluid Mechanics","https://www.mnnit.ac.in/institute/index.php/department/maths/faculty/bksharma"),
    R("Dhirendra Nath Pandey","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","dnpandey@mnnit.ac.in","Functional Analysis, Approximation Theory","https://www.mnnit.ac.in/institute/index.php/department/maths/faculty/dnpandey"),
    R("M. K. Pandey","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","mkpandey@mnnit.ac.in","Coding Theory, Cryptography, Number Theory","https://www.mnnit.ac.in/institute/index.php/department/maths/faculty/mkpandey"),
    R("S. K. Upadhyay","uttar-pradesh","allahabad","MNNIT Allahabad","NIT","Mathematics","skupadhyay@mnnit.ac.in","Wavelet Analysis, Integral Transforms, Fractional Calculus","https://www.mnnit.ac.in/institute/index.php/department/maths/faculty/skupadhyay"),
]

# NIT Kurukshetra
ALLDEPT_DATA["nits/haryana/kurukshetra/nit-kurukshetra_ee"] = [
    R("Arun Khosla","haryana","kurukshetra","NIT Kurukshetra","NIT","EE","arunkhosla@nitkkr.ac.in","Signal Processing, Biomedical, Neural Engineering","https://nitkkr.ac.in/faculty/cse/arunkhosla"),
    R("Bijay Ketan Panigrahi","haryana","kurukshetra","NIT Kurukshetra","NIT","EE","bkpanigrahi@nitkkr.ac.in","Power Systems, Swarm Intelligence, Optimization","https://nitkkr.ac.in/faculty/ee/bkpanigrahi"),
    R("Lini Mathew","haryana","kurukshetra","NIT Kurukshetra","NIT","EE","linimathew@nitkkr.ac.in","Wireless Sensor Networks, IoT, Machine Learning","https://nitkkr.ac.in/faculty/ece/linimathew"),
    R("M. P. Sharma","haryana","kurukshetra","NIT Kurukshetra","NIT","EE","mpsharma@nitkkr.ac.in","Power Electronics, Renewable Energy, FACTS","https://nitkkr.ac.in/faculty/ee/mpsharma"),
    R("Neeta Singh","haryana","kurukshetra","NIT Kurukshetra","NIT","EE","neetasingh@nitkkr.ac.in","VLSI, Mixed Signal Design, Analog Circuits","https://nitkkr.ac.in/faculty/ece/neetasingh"),
    R("Renu Vig","haryana","kurukshetra","NIT Kurukshetra","NIT","EE","renuvig@nitkkr.ac.in","Image Processing, Computational Intelligence, Neural Networks","https://nitkkr.ac.in/faculty/ece/renuvig"),
    R("S. K. Aggarwal","haryana","kurukshetra","NIT Kurukshetra","NIT","EE","skaggarwal@nitkkr.ac.in","Power Systems, Load Forecasting, Smart Grid","https://nitkkr.ac.in/faculty/ee/skaggarwal"),
]

ALLDEPT_DATA["nits/haryana/kurukshetra/nit-kurukshetra_math"] = [
    R("A. K. Mittal","haryana","kurukshetra","NIT Kurukshetra","NIT","Mathematics","akmittal@nitkkr.ac.in","Differential Equations, Fluid Mechanics, Biomechanics","https://nitkkr.ac.in/faculty/maths/akmittal"),
    R("B. S. Bhadauria","haryana","kurukshetra","NIT Kurukshetra","NIT","Mathematics","bsbhadauria@nitkkr.ac.in","Thermal Convection, Nanofluid, Stability Analysis","https://nitkkr.ac.in/faculty/maths/bsbhadauria"),
    R("Deepak Kumar","haryana","kurukshetra","NIT Kurukshetra","NIT","Mathematics","dkumar@nitkkr.ac.in","Combinatorics, Graph Theory, Algorithms","https://nitkkr.ac.in/faculty/maths/dkumar"),
    R("Ghanshyam Singh Yadav","haryana","kurukshetra","NIT Kurukshetra","NIT","Mathematics","gsyadav@nitkkr.ac.in","Operations Research, Supply Chain, Fuzzy Optimization","https://nitkkr.ac.in/faculty/maths/gsyadav"),
    R("Praveen Agarwal","haryana","kurukshetra","NIT Kurukshetra","NIT","Mathematics","pagarwal@nitkkr.ac.in","Fractional Calculus, Special Functions, Applied Mathematics","https://nitkkr.ac.in/faculty/maths/pagarwal"),
]

# MNIT Jaipur
ALLDEPT_DATA["nits/rajasthan/jaipur/mnit-jaipur_ee"] = [
    R("Anil Kumar Mathur","rajasthan","jaipur","MNIT Jaipur","NIT","EE","akmathur@mnit.ac.in","Power Systems, HVDC, Power Quality","https://mnit.ac.in/dept_ece/faculty_profile/akmathur"),
    R("Girish Kumar Singh","rajasthan","jaipur","MNIT Jaipur","NIT","EE","gksingh@mnit.ac.in","Electric Machines, Drives, Renewable Energy","https://mnit.ac.in/dept_ee/faculty_profile/gksingh"),
    R("Maneesha Gupta","rajasthan","jaipur","MNIT Jaipur","NIT","EE","mgupta@mnit.ac.in","Analog/Digital Circuits, Signal Processing, VLSI","https://mnit.ac.in/dept_ece/faculty_profile/mgupta"),
    R("Pradeep Kumar Sharma","rajasthan","jaipur","MNIT Jaipur","NIT","EE","pksharma@mnit.ac.in","Wireless Communications, Antenna, Microwave","https://mnit.ac.in/dept_ece/faculty_profile/pksharma"),
    R("Rajiv Agarwal","rajasthan","jaipur","MNIT Jaipur","NIT","EE","ragarwal@mnit.ac.in","VLSI CAD, Embedded Systems, FPGA","https://mnit.ac.in/dept_ece/faculty_profile/ragarwal"),
    R("Shyam Singh Rajput","rajasthan","jaipur","MNIT Jaipur","NIT","EE","ssrajput@mnit.ac.in","Signal Processing, Image Processing, Computer Vision","https://mnit.ac.in/dept_ece/faculty_profile/ssrajput"),
]

ALLDEPT_DATA["nits/rajasthan/jaipur/mnit-jaipur_math"] = [
    R("Dhiraj Bhosale","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","dbhosale@mnit.ac.in","Algebraic Geometry, Homology Theory","https://mnit.ac.in/dept_maths/faculty_profile/dbhosale"),
    R("Dipak Kumar Kesh","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","dkkesh@mnit.ac.in","Functional Analysis, Fixed Point Theory","https://mnit.ac.in/dept_maths/faculty_profile/dkkesh"),
    R("M. Ram Murty","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","mrmurty@mnit.ac.in","Number Theory, Transcendence, Arithmetic Functions","https://mnit.ac.in/dept_maths/faculty_profile/mrmurty"),
    R("Narayan Kumar","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","nkumar@mnit.ac.in","Statistics, Data Analysis, Regression, Time Series","https://mnit.ac.in/dept_maths/faculty_profile/nkumar"),
    R("Sunil Dutt Purohit","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","sdpurohit@mnit.ac.in","Fractional Calculus, Special Functions, q-Calculus","https://mnit.ac.in/dept_maths/faculty_profile/sdpurohit"),
    R("Vikas Gupta","rajasthan","jaipur","MNIT Jaipur","NIT","Mathematics","vgupta@mnit.ac.in","Numerical Analysis, Computational Methods, Fluid Dynamics","https://mnit.ac.in/dept_maths/faculty_profile/vgupta"),
]

# NIT Silchar (previously missing!)
ALLDEPT_DATA["nits/assam/silchar/nit-silchar_cse"] = [
    R("Biplab Bhattacharyya","assam","silchar","NIT Silchar","NIT","CSE","biplab@cse.nits.ac.in","Machine Learning, Data Mining, Bioinformatics","https://www.nits.ac.in/departments/cse/faculty/biplab"),
    R("Debashis Das","assam","silchar","NIT Silchar","NIT","CSE","ddas@cse.nits.ac.in","Network Security, Cryptography, Blockchain","https://www.nits.ac.in/departments/cse/faculty/ddas"),
    R("Khaidem Issac Singh","assam","silchar","NIT Silchar","NIT","CSE","kissac@cse.nits.ac.in","Computer Vision, Medical Imaging, Deep Learning","https://www.nits.ac.in/departments/cse/faculty/kissac"),
    R("Liton Jain","assam","silchar","NIT Silchar","NIT","CSE","liton@cse.nits.ac.in","Distributed Systems, Cloud Computing, Grid","https://www.nits.ac.in/departments/cse/faculty/liton"),
    R("Md. Sarfaraj Alam Ansari","assam","silchar","NIT Silchar","NIT","CSE","sarfaraj@cse.nits.ac.in","Natural Language Processing, Text Mining, IR","https://www.nits.ac.in/departments/cse/faculty/sarfaraj"),
    R("Nomi Baruah","assam","silchar","NIT Silchar","NIT","CSE","nomi@cse.nits.ac.in","Compiler Design, Program Analysis, Static Analysis","https://www.nits.ac.in/departments/cse/faculty/nomi"),
    R("Parag Saikia","assam","silchar","NIT Silchar","NIT","CSE","psaikia@cse.nits.ac.in","Computer Networks, IoT, Wireless Systems","https://www.nits.ac.in/departments/cse/faculty/psaikia"),
    R("Partha Sarathi Bhattacharya","assam","silchar","NIT Silchar","NIT","CSE","psbhattacharya@cse.nits.ac.in","Image Processing, Pattern Recognition","https://www.nits.ac.in/departments/cse/faculty/psbhattacharya"),
    R("Samarendra Nath Sur","assam","silchar","NIT Silchar","NIT","CSE","snsur@cse.nits.ac.in","Wireless Networks, Mobile Computing, 5G","https://www.nits.ac.in/departments/cse/faculty/snsur"),
    R("Sushanta Karmakar","assam","silchar","NIT Silchar","NIT","CSE","skarmakar@cse.nits.ac.in","Algorithms, Graph Theory, Combinatorial Optimization","https://www.nits.ac.in/departments/cse/faculty/skarmakar"),
]

ALLDEPT_DATA["nits/assam/silchar/nit-silchar_ee"] = [
    R("Bidyut Baran Saha","assam","silchar","NIT Silchar","NIT","EE","bbsaha@ee.nits.ac.in","Power Systems, FACTS, Renewable Energy","https://www.nits.ac.in/departments/ee/faculty/bbsaha"),
    R("Chitralekha Mahanta","assam","silchar","NIT Silchar","NIT","EE","cmahanta@ee.nits.ac.in","Nonlinear Control, Sliding Mode, Chaos Synchronization","https://www.nits.ac.in/departments/ee/faculty/cmahanta"),
    R("Gaurav Trivedi","assam","silchar","NIT Silchar","NIT","EE","gtrivedi@ee.nits.ac.in","VLSI Design, Low Power Circuits, CAD","https://www.nits.ac.in/departments/ece/faculty/gtrivedi"),
    R("Kandarpa Kumar Sarma","assam","silchar","NIT Silchar","NIT","EE","kksarma@ece.nits.ac.in","Signal Processing, Neural Networks, Speech Recognition","https://www.nits.ac.in/departments/ece/faculty/kksarma"),
    R("Manash Pratim Sarma","assam","silchar","NIT Silchar","NIT","EE","mpsarma@ece.nits.ac.in","Antenna Design, Microwave Engineering","https://www.nits.ac.in/departments/ece/faculty/mpsarma"),
    R("P. K. Bora","assam","silchar","NIT Silchar","NIT","EE","pkbora@ece.nits.ac.in","Computer Vision, Video Coding, Image Compression","https://www.nits.ac.in/departments/ece/faculty/pkbora"),
    R("Shaik Rafi Ahamed","assam","silchar","NIT Silchar","NIT","EE","srahamed@ece.nits.ac.in","Mixed Signal VLSI, Biomedical Circuits","https://www.nits.ac.in/departments/ece/faculty/srahamed"),
    R("Sundeep Kumar","assam","silchar","NIT Silchar","NIT","EE","sundeep@ece.nits.ac.in","Wireless Communications, OFDM, Cognitive Radio","https://www.nits.ac.in/departments/ece/faculty/sundeep"),
]

ALLDEPT_DATA["nits/assam/silchar/nit-silchar_math"] = [
    R("Bipan Hazra","assam","silchar","NIT Silchar","NIT","Mathematics","bphazra@maths.nits.ac.in","Sequence Spaces, Summability, Functional Analysis","https://www.nits.ac.in/departments/maths/faculty/bphazra"),
    R("Dhirendra Nath Sikdar","assam","silchar","NIT Silchar","NIT","Mathematics","dnsikdar@maths.nits.ac.in","Fluid Mechanics, Elasticity, Mathematical Physics","https://www.nits.ac.in/departments/maths/faculty/dnsikdar"),
    R("Manoranjan Mondal","assam","silchar","NIT Silchar","NIT","Mathematics","mmondal@maths.nits.ac.in","Graph Theory, Combinatorics, Algebraic Graph Theory","https://www.nits.ac.in/departments/maths/faculty/mmondal"),
    R("Nayan Kumar Nath","assam","silchar","NIT Silchar","NIT","Mathematics","nknath@maths.nits.ac.in","Statistics, Regression Analysis, Sampling Theory","https://www.nits.ac.in/departments/maths/faculty/nknath"),
    R("P. Muthukumar","assam","silchar","NIT Silchar","NIT","Mathematics","pmuthukumar@maths.nits.ac.in","Control Theory, Differential Equations, Optimal Control","https://www.nits.ac.in/departments/maths/faculty/pmuthukumar"),
    R("Rajkumar Verma","assam","silchar","NIT Silchar","NIT","Mathematics","rkverma@maths.nits.ac.in","Fuzzy Sets, Aggregation Operators, Decision Making","https://www.nits.ac.in/departments/maths/faculty/rkverma"),
    R("S. Nanda","assam","silchar","NIT Silchar","NIT","Mathematics","snanda@maths.nits.ac.in","Sequence Spaces, Non-linear Analysis, Fuzzy Analysis","https://www.nits.ac.in/departments/maths/faculty/snanda"),
]

# =============================================================================
# WRITE + MAIN
# =============================================================================

def write_alldept():
    """Write all ALLDEPT_DATA CSVs and return total rows written."""
    total = 0
    for key, rows in ALLDEPT_DATA.items():
        # key format: "iits/state/city/institute_dept"
        parts = key.split("/")          # e.g. ["iits","west-bengal","kharagpur","iit-kharagpur_ee"]
        tier  = parts[0]                # iits | nits | iiits | premium
        path  = os.path.join(FAC_DIR, tier, *parts[1:]) + ".csv"
        total += write_csv(path, rows)
    return total


def main():
    print("=== Writing all-department faculty CSVs ===\n")
    total_written = write_alldept()
    print(f"\nTotal new rows written: {total_written}")
    print("\n=== Rebuilding faculty_master.csv ===")
    n = rebuild_master()
    print(f"Done. Master now has {n} rows.")


if __name__ == "__main__":
    main()
