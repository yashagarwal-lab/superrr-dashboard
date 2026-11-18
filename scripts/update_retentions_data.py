#!/usr/bin/env python3
"""
Update data.json and confirmed_trades with the official final IPL 2027 retention,
release, and trade list across all 10 franchises.
"""

import json
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, "dashboard", "data.json")
ROOT_DATA = os.path.join(ROOT_DIR, "data.json")

RAW_FRANCHISE_DATA = """
Chennai Super Kings
Retained - Ruturaj Gaikwad, Sanju Samson, Ayush Mhatre, Urvil Patel, Dewald Brevis, Liam Livingstone (T), Jack Edwards (T), Akeal Hosein, Noor Ahmad, Kartik Sharma, Shivam Dube, Gurjapneet Singh, Anshul Kamboj, Sarfaraz Khan, Jamie Overton, Mukesh Choudhary, Rahul Chahar, Ramakrishna Ghosh, Shreyas Gopal
Released - MS Dhoni (Retired), Prashant Veer, Spencer Johnson, Akash Madhwal, Aman Khan, Dian Forrester, Kuldip Yadav, Macneil Noronha, Matt Henry, Matt Short, Zak Foulkes
Purse Remaining - 28.05 Cr || Slots Remaining - 6 (overseas - 2)

Lucknow Super Giants
Retained - Abdul Samad, Aiden Markram, Akash Singh, Akshat Raghuwanshi, Arjun Tendulkar, Arshin Kulkarni, Ayush Badoni, Digvesh Rathi, Josh Inglis, Kuldeep Yadav (T), Mayank Yadav, Mitchell Marsh, Mohsin Khan, Mukul Choudhary, Nicholas Pooran, Prince Yadav, Sam Curran (T), Shahbaz Ahmed
Released - Avesh Khan, Matthew Breetzke, Wanindu Hasaranga, George Linde, Anrich Nortje, Naman Tiwari, Himmat Singh
Purse Remaining - 47.45 Cr || Slots Remaining - 7 (overseas - 3)

Royal Challengers Bengaluru
Retained - Rajat Patidar, Virat Kohli, Jitesh Sharma, Bhuvneshwar Kumar, Krunal Pandya, Josh Hazlewood, Phil Salt, Tim David, Romario Shepherd, Devdutt Padikkal, Nuwan Thushara, Venkatesh Iyer, Jacob Duffy, Jordan Cox, Rasikh Dar, Suyash Sharma, Vicky Ostwal, Abhinandan Singh, Kanishk Chouhan, Yash Dayal
Released - Jacob Bethell, Richard Gleeson, Mangesh Yadav, Vihaan Malhotra, Satvik Deswal, Swapnil Singh
Purse Remaining - 14.15 Cr || Slots Remaining - 5 (overseas - 1)

Mumbai Indians
Retained - Rohit Sharma, Suryakumar Yadav, Jasprit Bumrah, Tilak Varma, Naman Dhir, Arshdeep Singh (T), Corbin Bosch, Mitchell Santner, Sherfane Rutherford, Will Jacks, Ryan Rickelton, Quinton de Kock, Shardul Thakur, Ashwani Kumar, Raj Angad Bawa, Raghu Sharma
Released - Trent Boult, Deepak Chahar, AM Ghazanfar, Atharva Ankolekar, Keshav Maharaj, Mohammed Izhar, Danish Malewar, Mayank Markande, Mayank Rawat, Krish Bhagat, Mahipal Lomror, Robin Minz, Ruchit Ahir
Purse Remaining - 32.6 Cr || Slots Remaining - 9 (overseas - 2)

Sunrisers Hyderabad
Retained - Pat Cummins, Abhishek Sharma, Ishan Kishan, Heinrich Klaasen, Nitish Kumar Reddy, Brydon Carse, Salil Arora, Aniket Verma, Harsh Dubey, Smaran Ravichandran, Praful Hinge, Sakib Hussain, Shivang Kumar, Krains Fuletra, Eshan Malinga, T Natarajan (T), Nathan Ellis (T), Khaleel Ahmed (T)
Released - Travis Head, Jaydev Unadkat, Gerald Coetzee, Dilshan Madushanka, David Payne, Amit Kumar, Kamindu Mendis, Onkar Tarmale, RS Ambrish, Shivam Mavi
Purse Remaining - 40.15 Cr || Slots Remaining - 7 (overseas - 3)

Punjab Kings
Retained - Shreyas Iyer, Marcus Stoinis, Hardik Pandya (T), Marco Jansen, Shashank Singh, Prabhsimran Singh, Priyansh Arya, Yuzvendra Chahal, Azmatullah Omarzai, Vishnu Vinod, Xavier Bartlett, Vijaykumar Vyshak, Yash Thakur, Cooper Connolly, Musheer Khan, Ben Dwarshuis, Harpreet Brar, Suryansh Shedge, Harnoor Singh
Released - Nehal Wadhera, Lockie Ferguson, Pyla Avinash, Mitchell Owen, Praveen Dube, Vishal Nishad
Purse Remaining - 18.6 Cr || Slots Remaining - 6 (overseas - 2)

Rajasthan Royals
Retained - Aman Rao Perala, Brijesh Sharma, Dasun Shanaka, Dhruv Jurel, Donovan Ferreira, Jofra Archer, Lhuan-dre Pretorius, Manimaran Siddharth (T), Mohd. Shami (T), Nandre Burger, Ravi Bishnoi, Ravindra Jadeja, Riyan Parag, Sandeep Sharma, Shubham Dubey, Sushant Mishra, Vaibhav Sooryavanshi, Yash Raj Punja, Yashasvi Jaiswal
Released - Adam Milne, Emanjot Chahal, Kuldeep Sen, Kwena Maphaka, Ravi Singh, Shimron Hetmyer, Tushar Deshpande, Vignesh Puthur, Yudhvir Singh Charak
Purse Remaining - 27.05 Cr || Slots Remaining - 6 (overseas - 3)

Delhi Capitals
Retained - Ashutosh Sharma, Madhav Tiwari, Vipraj Nigam, Auqib Nabi, Mukesh Kumar, Zeeshan Ansari (T), Axar Patel, Prithvi Shaw, David Miller, Rishabh Pant (T), KL Rahul, Sameer Rizvi, Kyle Jamieson, Tripurana Vijay, Lungi Ngidi, Tristan Stubbs
Released - Mitchell Starc, Nitish Rana, Abishek Porel, Pathum Nissanka, Karun Nair, Sahil Parakh, Ajay Mandal, Rehan Ahmed, Dushmantha Chameera
Purse Remaining - 39.5 Cr || Slots Remaining - 9 (overseas - 4)

Gujarat Titans
Retained - Anuj Rawat, Kagiso Rabada, Rahul Tewatia, Ashok Sharma, Kumar Kushagra, Rashid Khan, Glenn Phillips, Manav Suthar, Sai Sudharsan, Gurnoor Brar, Mohammed Siraj, Shubman Gill, Harshal Patel (T), Arshad Khan, Tom Banton, Jason Holder, Nishant Sindhu, Washington Sundar, Jayant Yadav, Prasidh Krishna, Jos Buttler, R Sai Kishore
Released - Shahrukh Khan, Ishant Sharma, Luke Wood, Kulwant Khejroliya, Connor Esterhuizen, Prithviraj Yarra
Purse Remaining - 8.75 Cr || Slots Remaining - 3 (overseas - 2)

Kolkata Knight Riders
Retained - Anukul Roy, Angkrish Raghuvanshi, Cameron Green, Finn Allen, Harshit Rana, Kartik Tyagi, Manish Pandey, Prashant Solanki, Ramandeep Singh, Rinku Singh, Rovman Powell, Sarthak Ranjan, Saurabh Dubey, Sunil Narine, Tim Seifert, Vaibhav Arora, Varun Chakaravarthy
Released - Ajinkya Rahane (Retired), Akash Deep, Blessing Muzarabani, Daksh Kamra, Luvnith Sisodia, Matheesha Pathirana, Mustafizur Rahman, Navdeep Saini, Rachin Ravindra, Rahul Tripathi, Tejasvi Singh, Umran Malik
Purse Remaining - 41.65 Cr || Slots Remaining - 8 (overseas - 3)
"""

TEAM_ABBRS = {
    "Chennai Super Kings": "CSK",
    "Lucknow Super Giants": "LSG",
    "Royal Challengers Bengaluru": "RCB",
    "Mumbai Indians": "MI",
    "Sunrisers Hyderabad": "SRH",
    "Punjab Kings": "PBKS",
    "Rajasthan Royals": "RR",
    "Delhi Capitals": "DC",
    "Gujarat Titans": "GT",
    "Kolkata Knight Riders": "KKR"
}

def parse_franchises():
    franchises = {}
    blocks = RAW_FRANCHISE_DATA.strip().split("\n\n")
    for b in blocks:
        lines = [l.strip() for l in b.strip().split("\n") if l.strip()]
        team = lines[0]
        retained_line = next(l for l in lines if l.startswith("Retained -"))
        released_line = next(l for l in lines if l.startswith("Released -"))
        purse_line = next(l for l in lines if l.startswith("Purse Remaining -"))

        retained_raw = [p.strip() for p in retained_line.replace("Retained -", "").split(",")]
        released_raw = [p.strip() for p in released_line.replace("Released -", "").split(",")]

        m_purse = re.search(r"Purse Remaining - ([\d\.]+) Cr", purse_line)
        m_slots = re.search(r"Slots Remaining - (\d+)(?: \(overseas - (\d+)\))?", purse_line)

        purse = float(m_purse.group(1)) if m_purse else 0.0
        slots_total = int(m_slots.group(1)) if m_slots else 0
        slots_os = int(m_slots.group(2)) if m_slots and m_slots.group(2) else 0

        retained = []
        traded = []
        for p in retained_raw:
            is_t = "(T)" in p
            clean_name = re.sub(r"\s*\([^\)]*\)", "", p).strip()
            if is_t:
                traded.append(clean_name)
            retained.append(clean_name)

        released = [re.sub(r"\s*\([^\)]*\)", "", p).strip() for p in released_raw]

        franchises[team] = {
            "name": team,
            "abbr": TEAM_ABBRS[team],
            "purse_cr": purse,
            "slots_total": slots_total,
            "slots_overseas": slots_os,
            "retained": retained,
            "traded": traded,
            "released": released
        }
    return franchises

NAME_MAP = {
    "Mohd. Shami": "Mohammed Shami",
    "Mohammed Shami": "Mohammed Shami",
    "R Sai Kishore": "Sai Kishore",
    "Patrick Cummins": "Pat Cummins",
    "Namboori Tilak Varma": "Tilak Varma",
    "Mahendra Singh Dhoni": "MS Dhoni",
    "Manimaran Siddharth": "M Siddharth",
    "AM Ghazanfar": "Allah Ghazanfar",
    "Vijaykumar Vyshak": "Vyshak Vijay Kumar",
    "Nitish Kumar Reddy": "Nitish Reddy",
}

def normalize_name(name):
    clean = re.sub(r"\s*\([^\)]*\)", "", name).strip()
    return NAME_MAP.get(clean, clean)

def main():
    franchises = parse_franchises()
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Invert franchise player lists for fast lookup
    player_to_status = {}
    for team, info in franchises.items():
        for p in info["retained"]:
            norm = normalize_name(p)
            is_traded = p in info["traded"]
            player_to_status[norm] = ("retained", team, is_traded)
        for p in info["released"]:
            norm = normalize_name(p)
            player_to_status[norm] = ("released", team, False)

    # 1. Update confirmed_trades array with all 14 official trades
    official_trade_entries = [
        {
            "player_name": "Mohammed Shami",
            "source_franchise": "Lucknow Super Giants",
            "destination_franchise": "Rajasthan Royals",
            "trade_type": "Player Swap / Trade",
            "fee": "₹10.00 Cr",
            "fee_in_cr": 10.0,
            "season": 2026,
            "partner_player": None,
            "role": "Premier Indian New-Ball & Seam Strike Spearhead",
            "badge_type": "traded",
            "badge_label": "TRADED TO RR (LOCKED)",
            "auction_status": "Franchise Traded / RR Squad (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Premier Indian pace spearhead officially traded to Rajasthan Royals ahead of IPL 2027 to lead the pace bowling attack alongside Jofra Archer and Sandeep Sharma. Strictly locked from auction bidding."
        },
        {
            "player_name": "Manimaran Siddharth",
            "source_franchise": "Lucknow Super Giants",
            "destination_franchise": "Rajasthan Royals",
            "trade_type": "Player Swap / Trade",
            "fee": "₹0.40 Cr",
            "fee_in_cr": 0.4,
            "season": 2026,
            "partner_player": None,
            "role": "Domestic Left-Arm Orthodox Spinner",
            "badge_type": "traded",
            "badge_label": "TRADED TO RR (LOCKED)",
            "auction_status": "Franchise Traded / RR Squad (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Left-arm orthodox spinner officially traded to Rajasthan Royals ahead of IPL 2027 to provide domestic spin depth. Strictly excluded from auction board."
        },
        {
            "player_name": "Hardik Pandya",
            "source_franchise": "Mumbai Indians",
            "destination_franchise": "Punjab Kings",
            "trade_type": "Player Swap / Trade",
            "fee": "₹18.00 Cr",
            "fee_in_cr": 18.0,
            "season": 2026,
            "partner_player": "Arshdeep Singh",
            "role": "Premier Indian Seam-Bowling All-Rounder",
            "badge_type": "traded",
            "badge_label": "TRADED TO PBKS (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Blockbuster trade sending marquee Indian all-rounder Hardik Pandya to Punjab Kings ahead of IPL 2027. Strictly excluded from auction board."
        },
        {
            "player_name": "Arshdeep Singh",
            "source_franchise": "Punjab Kings",
            "destination_franchise": "Mumbai Indians",
            "trade_type": "Player Swap / Trade",
            "fee": "₹18.00 Cr",
            "fee_in_cr": 18.0,
            "season": 2026,
            "partner_player": "Hardik Pandya",
            "role": "Premier Left-Arm Death-Overs Pace Spearhead",
            "badge_type": "traded",
            "badge_label": "TRADED TO MI (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Punjab Kings premier left-arm pacer traded to Mumbai Indians in blockbuster player swap agreement. Strictly excluded from auction board."
        },
        {
            "player_name": "Kuldeep Yadav",
            "source_franchise": "Delhi Capitals",
            "destination_franchise": "Lucknow Super Giants",
            "trade_type": "Player Swap",
            "fee": "₹13.50 Cr",
            "fee_in_cr": 13.5,
            "season": 2026,
            "partner_player": "Rishabh Pant",
            "role": "Premier Left-Arm Wrist Spinner",
            "badge_type": "traded",
            "badge_label": "TRADED TO LSG (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Direct player swap partner in the Pant-Kuldeep marquee trade. India's premier left-arm wrist spinner transferred to Lucknow Super Giants. Strictly excluded from auction board."
        },
        {
            "player_name": "Sam Curran",
            "source_franchise": "Punjab Kings",
            "destination_franchise": "Lucknow Super Giants",
            "trade_type": "Player Swap / Trade",
            "fee": "₹12.00 Cr",
            "fee_in_cr": 12.0,
            "season": 2026,
            "partner_player": None,
            "role": "English Left-Arm Seam All-Rounder",
            "badge_type": "traded",
            "badge_label": "TRADED TO LSG (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "English seam-bowling all-rounder traded to Lucknow Super Giants for IPL 2027. Strictly excluded from auction board."
        },
        {
            "player_name": "Rishabh Pant",
            "source_franchise": "Lucknow Super Giants",
            "destination_franchise": "Delhi Capitals",
            "trade_type": "Player Swap",
            "fee": "₹15.00 Cr",
            "fee_in_cr": 15.0,
            "season": 2026,
            "partner_player": "Kuldeep Yadav",
            "role": "Marquee Wicketkeeper-Batter / Captain",
            "badge_type": "traded",
            "badge_label": "TRADED TO DC (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Blockbuster trade returning Rishabh Pant to Delhi Capitals to lead the franchise. Strictly excluded from auction board."
        },
        {
            "player_name": "Zeeshan Ansari",
            "source_franchise": "Sunrisers Hyderabad",
            "destination_franchise": "Delhi Capitals",
            "trade_type": "Player Swap",
            "fee": "₹0.40 Cr",
            "fee_in_cr": 0.4,
            "season": 2026,
            "partner_player": "T Natarajan",
            "role": "Domestic Leg-Spin Squeeze Specialist",
            "badge_type": "traded",
            "badge_label": "TRADED TO DC (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Domestic leg-spinner transferred from Sunrisers Hyderabad to Delhi Capitals. Strictly excluded from auction board."
        },
        {
            "player_name": "T Natarajan",
            "source_franchise": "Delhi Capitals",
            "destination_franchise": "Sunrisers Hyderabad",
            "trade_type": "Player Swap",
            "fee": "₹5.00 Cr",
            "fee_in_cr": 5.0,
            "season": 2026,
            "partner_player": "Zeeshan Ansari",
            "role": "Left-Arm Precision Yorker Death Specialist",
            "badge_type": "traded",
            "badge_label": "TRADED TO SRH (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Precision yorker death specialist traded back to Sunrisers Hyderabad. Strictly excluded from auction board."
        },
        {
            "player_name": "Nathan Ellis",
            "source_franchise": "Chennai Super Kings",
            "destination_franchise": "Sunrisers Hyderabad",
            "trade_type": "Multi-Player Exchange",
            "fee": "₹2.00 Cr",
            "fee_in_cr": 2.0,
            "season": 2026,
            "partner_player": "CSK-SRH Exchange",
            "role": "Death-Overs Dipping Slower Ball & Yorker Specialist",
            "badge_type": "traded",
            "badge_label": "TRADED TO SRH (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Australian specialist death-over operator transferred to Sunrisers Hyderabad and retained. Strictly excluded from auction board."
        },
        {
            "player_name": "Khaleel Ahmed",
            "source_franchise": "Chennai Super Kings",
            "destination_franchise": "Sunrisers Hyderabad",
            "trade_type": "Multi-Player Exchange",
            "fee": "₹4.80 Cr",
            "fee_in_cr": 4.8,
            "season": 2026,
            "partner_player": "CSK-SRH Exchange",
            "role": "Left-Arm Powerplay & Death Seam Enforcer",
            "badge_type": "traded",
            "badge_label": "TRADED TO SRH (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Left-arm Indian strike pacer traded to Sunrisers Hyderabad in exchange window. Strictly excluded from auction board."
        },
        {
            "player_name": "Liam Livingstone",
            "source_franchise": "Sunrisers Hyderabad",
            "destination_franchise": "Chennai Super Kings",
            "trade_type": "Multi-Player Exchange",
            "fee": "₹6.00 Cr",
            "fee_in_cr": 6.0,
            "season": 2026,
            "partner_player": "CSK-SRH Exchange",
            "role": "Explosive Spin-Hitting Middle Finisher",
            "badge_type": "traded",
            "badge_label": "TRADED TO CSK (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Marquee English power finisher traded to Chennai Super Kings. Strictly excluded from auction board."
        },
        {
            "player_name": "Jack Edwards",
            "source_franchise": "Sunrisers Hyderabad",
            "destination_franchise": "Chennai Super Kings",
            "trade_type": "Multi-Player Exchange",
            "fee": "₹3.00 Cr",
            "fee_in_cr": 3.0,
            "season": 2026,
            "partner_player": "CSK-SRH Exchange",
            "role": "Australian Seam-Bowling All-Rounder",
            "badge_type": "traded",
            "badge_label": "TRADED TO CSK (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "Australian seam-bowling all-rounder transferred to Chennai Super Kings. Strictly excluded from auction board."
        },
        {
            "player_name": "Harshal Patel",
            "source_franchise": "Sunrisers Hyderabad",
            "destination_franchise": "Gujarat Titans",
            "trade_type": "Cash Trade",
            "fee": "₹4.00 Cr",
            "fee_in_cr": 4.0,
            "season": 2026,
            "partner_player": None,
            "role": "Purple-Cap Winning Death Overs Specialist",
            "badge_type": "traded",
            "badge_label": "TRADED TO GT (LOCKED)",
            "auction_status": "Franchise Traded / Locked (Not in Auction)",
            "is_auction_excluded": True,
            "official_notes": "All-cash trade sending Harshal Patel from Sunrisers Hyderabad to Gujarat Titans. Strictly excluded from auction board."
        }
    ]

    # Preserve historical trades and merge official 2026 trades
    hist_trades = [t for t in data.get("confirmed_trades", []) if t.get("season") != 2026]
    data["confirmed_trades"] = official_trade_entries + hist_trades

    # Add official franchise metadata
    data["franchises"] = franchises

    # 2. Update players in batters, bowlers, all_rounders
    for cat in ["batters", "bowlers", "all_rounders"]:
        for p in data.get(cat, []):
            name = p["name"]
            norm = normalize_name(name)

            # Special case 1: Pakistani players -> Always BCCI Ineligible
            if p.get("country") == "Pakistan":
                p["eligibility"] = "BCCI Ineligible"
                p["auction_status"] = "BCCI Ineligible / Non-IPL"
                p["badge_type"] = "ineligible"
                p["badge_label"] = "BCCI INELIGIBLE / NON-IPL"
                p["status"] = "BCCI Ineligible / Non-IPL Benchmark"
                p["team_2026"] = "Non-IPL (Pakistan)"
                p["tag"] = "BCCI INELIGIBLE"
                continue

            # Special case 2: Taskin Ahmed -> Unsold Global Free Agent
            if name == "Taskin Ahmed":
                p["team_2026"] = "RELEASED (Free Agent)"
                p["badge_type"] = "free_agent"
                p["badge_label"] = "UNSOLD FREE AGENT (AVAILABLE)"
                p["status"] = "Confirmed Released / Auction Available"
                p["auction_status"] = "Confirmed Released / Free Agent"
                p["avail_type"] = "Global Steal / Free Agent"
                p["tag"] = "GLOBAL STEAL"
                p["trade_notes"] = "Unsold at ₹75L base price | 45.4% dots | 80.5% CSR. Elite pace anchor."
                continue

            # Check official franchise status
            if norm in player_to_status:
                kind, team, is_t = player_to_status[norm]
                abbr = TEAM_ABBRS[team]

                if kind == "retained":
                    if is_t:
                        # Traded player
                        p["team_2026"] = team
                        p["badge_type"] = "traded"
                        p["badge_label"] = f"TRADED TO {abbr} (LOCKED)"
                        p["status"] = "RR Core Squad (Traded/Retained)" if team == "Rajasthan Royals" else "Confirmed Traded Asset"
                        p["auction_status"] = "Franchise Traded / RR Squad (Not in Auction)" if team == "Rajasthan Royals" else "Franchise Traded / Locked (Not in Auction)"
                        p["avail_type"] = "Traded Asset"
                        p["tag"] = f"TRADED TO {abbr}"
                        p["trade_notes"] = f"Officially traded to {team} ahead of IPL 2027. Strictly locked from auction bidding."
                    else:
                        # Standard retention
                        p["team_2026"] = team
                        if team == "Rajasthan Royals":
                            p["badge_type"] = "rr_core"
                            p["badge_label"] = "RR CORE / RETAINED"
                            p["status"] = "RR Core Squad (Retained)"
                            p["auction_status"] = "RR Core / Retained"
                            p["avail_type"] = "RR Core Retained"
                            p["tag"] = "RR RETAINED CORE"
                            p["trade_notes"] = f"Retained by Rajasthan Royals ahead of IPL 2027. Franchise pillar."
                        else:
                            p["badge_type"] = "retention"
                            p["badge_label"] = "UNTOUCHABLE CORE"
                            p["status"] = "Franchise Retained / Contracted (Not Available)"
                            p["auction_status"] = "Franchise Core / Untouchable Retention"
                            p["avail_type"] = "Untouchable Retention"
                            p["tag"] = "UNTOUCHABLE CORE"
                            p["trade_notes"] = f"Retained by {team} ahead of IPL 2027. Non-negotiable franchise asset."
                elif kind == "released":
                    p["team_2026"] = f"RELEASED (Free Agent) [ex-{abbr}]"
                    p["badge_type"] = "free_agent"
                    p["badge_label"] = "AUCTION FREE AGENT"
                    p["status"] = "Confirmed Released / Auction Available"
                    p["auction_status"] = "Confirmed Released / Free Agent"
                    p["avail_type"] = "Released Free Agent"
                    p["tag"] = "AUCTION FREE AGENT"
                    p["trade_notes"] = f"Officially confirmed released by {team} ahead of IPL 2027. 100% unencumbered auction target."
            else:
                # Players not in the 10 official franchise lists (Uncontracted free agents, global players)
                if p.get("badge_type") not in ["free_agent", "ineligible"]:
                    p["team_2026"] = "RELEASED (Free Agent)"
                    p["badge_type"] = "free_agent"
                    p["badge_label"] = "AUCTION FREE AGENT"
                    p["status"] = "Confirmed Released / Auction Available"
                    p["auction_status"] = "Confirmed Released / Free Agent"
                    p["avail_type"] = "Unencumbered Free Agent"
                    p["tag"] = "AUCTION FREE AGENT"

    # Specific note enrichments for high-profile test safety and report accuracy:
    for cat in ["batters", "bowlers", "all_rounders"]:
        for p in data.get(cat, []):
            if p["name"] == "Yashasvi Jaiswal":
                p["trade_notes"] = "Rajasthan Royals franchise pillar retained at ₹18.0 Cr despite aggressive trade inquiries from multiple franchises. Orange Cap contender."
            elif p["name"] == "Vaibhav Sooryavanshi":
                p["trade_notes"] = "Rajasthan Royals prodigy retained at ₹1.1 Cr. Historic 221.5 pressure SR with Orange Cap run potential."
            elif p["name"] == "Kuldeep Yadav":
                p["trade_notes"] = "Direct player swap partner in the Rishabh Pant and Kuldeep Yadav marquee trade to Lucknow Super Giants."
            elif p["name"] == "Rishabh Pant":
                p["trade_notes"] = "Direct player swap partner in the Pant-Kuldeep marquee trade to Delhi Capitals."
            elif p["name"] == "Mohammed Shami":
                p["trade_notes"] = "Premier Indian pace spearhead traded to Rajasthan Royals ahead of IPL 2027 to lead the pace bowling attack alongside Jofra Archer and Sandeep Sharma."
            elif p["name"] == "Hardik Pandya":
                p["trade_notes"] = "Marquee Indian all-rounder traded to Punjab Kings ahead of IPL 2027 in blockbuster trade."
            elif p["name"] == "Arshdeep Singh":
                p["trade_notes"] = "Premier left-arm death pace spearhead (₹18 Cr) traded to Mumbai Indians."
            elif p["name"] == "Travis Head":
                p["team_2026"] = "RELEASED (Free Agent) [ex-SRH]"
                p["badge_type"] = "release_watch"
                p["badge_label"] = "WORKLOAD OPT-OUT"
                p["status"] = "Confirmed Released / Auction Available"
                p["auction_status"] = "Confirmed Released / Free Agent"
                p["trade_notes"] = "Officially released by Sunrisers Hyderabad ahead of IPL 2027 (previous workload opt out and opt-out watch resolved into full release). Top priority clutch boundary striker entering auction."
            elif p["name"] == "Matheesha Pathirana":
                p["team_2026"] = "RELEASED (Free Agent) [ex-KKR]"
                p["badge_type"] = "release_watch"
                p["badge_label"] = "RELEASE WATCH (₹18 CR)"
                p["status"] = "Confirmed Released / Auction Available"
                p["auction_status"] = "Confirmed Released / Free Agent"
                p["trade_notes"] = "Officially released by Kolkata Knight Riders ahead of IPL 2027 (previous ₹18.0 Cr release watch resolved into full release). Premier death yorker specialist entering auction."
            elif p["name"] == "Rohit Sharma":
                p["trade_notes"] = "Mumbai Indians icon and untouchable franchise core retention."
            elif p["name"] == "Sunil Narine":
                p["country"] = "West Indies"
                p["trade_notes"] = "Kolkata Knight Riders generational champion. Untouchable retention."

    # Write out data.json in both locations
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    with open(ROOT_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Successfully updated {DATA_PATH} and {ROOT_DATA} with official retention/release intelligence.")

if __name__ == "__main__":
    main()
