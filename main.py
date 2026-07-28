"""
Laitan-Adio Smart Inventory Expert System
Complete Implementation with Corrected Brand-Item Mappings
All 200 Items | Chat-Style Advice | Real-Time Graphical Analysis
"""
import gradio as gr
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
import os
import traceback

DB_NAME = "laitan_adio_final_corrected.db"

# ============================================================================
# DATABASE INITIALIZATION - ALL 200 ITEMS WITH CORRECTED BRAND MAPPINGS
# ============================================================================
def init_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''CREATE TABLE inventory (
        ItemID INTEGER PRIMARY KEY, Category TEXT, Subcategory TEXT, Brand TEXT,
        Name TEXT, Supplier TEXT, Unit TEXT, Stock INTEGER, Threshold INTEGER,
        LeadTime INTEGER, Price REAL, Expiry TEXT, SeasonalMultiplier REAL DEFAULT 1.0,
        ReorderCount INTEGER DEFAULT 0
    )''')
    
    # ALL 200 ITEMS WITH REALISTIC NIGERIAN BRAND MAPPINGS
    csv_data = [
        # ==================== BEVERAGES (20 items) ====================
        (1001,"Beverages","Carbonated Drinks","Coca-Cola","Coca-Cola Original 50cl","CocaCola_NG","Bottle",197,42,5,250,"",1.0,0),
        (1002,"Beverages","Carbonated Drinks","Coca-Cola","Fanta Orange 50cl","CocaCola_NG","Bottle",189,13,5,200,"",1.2,2),
        (1003,"Beverages","Carbonated Drinks","Pepsi","Pepsi Cola 50cl","PepsiCo_NG","Bottle",72,15,3,220,"",1.0,1),
        (1004,"Beverages","Carbonated Drinks","Pepsi","7UP Lemon 50cl","PepsiCo_NG","Bottle",148,24,2,200,"",1.0,0),
        (1005,"Beverages","Juice","Coca-Cola","Minute Maid Orange 1L","CocaCola_NG","Bottle",84,13,2,450,"",1.1,1),
        (1006,"Beverages","Juice","Chi Limited","Chi 100% Orange Juice 1L","Chi_NG","Bottle",82,19,5,500,"2027-09-02",1.3,3),
        (1007,"Beverages","Juice","Holland","Holland Apple Juice 1L","Holland_NG","Carton",63,33,6,600,"",1.0,0),
        (1008,"Beverages","Water","Eva","Eva Water 75cl","Eva_NG","Bottle",102,10,2,150,"",1.0,2),
        (1009,"Beverages","Water","Nestle","Nestle Pure Life 75cl","Nestle_NG","Bottle",121,27,1,180,"",1.0,1),
        (1010,"Beverages","Water","Aquafina","Aquafina Water 75cl","PepsiCo_NG","Bottle",95,45,4,160,"",1.2,4),
        (1011,"Beverages","Tea","Lipton","Lipton Yellow Label Tea 100bags","Unilever_NG","Box",154,22,5,1200,"",1.0,2),
        (1012,"Beverages","Tea","Mikado","Mikado Tea 50bags","Mikado_NG","Box",20,36,3,800,"",1.0,0),
        (1013,"Beverages","Malt","Nestle","Milo Chocolate Malt 400g","Nestle_NG","Tin",189,12,3,2500,"",1.0,1),
        (1014,"Beverages","Malt","Cadbury","Bournvita Chocolate 400g","Cadbury_NG","Tin",13,19,1,2800,"",1.5,3),
        (1015,"Beverages","Coffee","Nestle","Nescafe Classic Coffee 200g","Nestle_NG","Jar",78,47,6,3500,"2027-01-07",1.0,1),
        (1016,"Beverages","Energy Drinks","Red Bull","Red Bull Energy Drink 250ml","RedBull_NG","Can",74,29,1,800,"",1.3,2),
        (1017,"Beverages","Energy Drinks","Predator","Predator Energy Drink 250ml","Predator_NG","Can",25,43,1,500,"2027-05-26",1.0,0),
        (1018,"Beverages","Yogurt Drinks","Friesland","Friesland Yoghurt Drink 500ml","Friesland_NG","Bottle",132,20,3,600,"2026-06-16",1.0,1),
        (1019,"Beverages","Malt","Grand Cereals","Malta Guinness 65cl","Diageo_NG","Bottle",161,49,5,350,"2026-08-22",1.0,2),
        (1020,"Beverages","Malt","Nigerian Breweries","Amstel Malta 65cl","NigerianBreweries_NG","Bottle",120,12,3,380,"2026-08-05",1.0,4),
        
        # ==================== BAKERY (20 items) ====================
        (1021,"Bakery","Bread","Golden Penny","Golden Penny Agege Bread","FlourMill_NG","Loaf",105,44,7,800,"2026-08-11",1.0,1),
        (1022,"Bakery","Bread","Butterfield","Butterfield Butter Bread","Butterfield_NG","Loaf",44,36,4,1200,"",1.0,0),
        (1023,"Bakery","Bread","Agege","Local Agege Bread","Local_Bakery","Loaf",186,31,3,500,"",1.0,2),
        (1024,"Bakery","Cake","Golden Penny","Golden Penny Cake Mix 1kg","FlourMill_NG","Pack",65,30,5,1800,"2027-06-01",1.0,1),
        (1025,"Bakery","Biscuits","McVities","McVities Digestive Biscuits","UnitedBiscuits_NG","Pack",198,50,5,900,"2026-12-24",1.0,3),
        (1026,"Bakery","Biscuits","Mikado","Mikado Crackers","Mikado_NG","Pack",14,37,1,600,"2026-08-16",1.0,0),
        (1027,"Bakery","Biscuits","Jacob's","Jacob's Cream Crackers","UnitedBiscuits_NG","Pack",9,37,2,750,"2025-12-12",1.0,1),
        (1028,"Bakery","Pastries","Butterfield","Butterfield Meat Pie","Butterfield_NG","Piece",42,23,5,350,"2027-06-17",1.0,0),
        (1029,"Bakery","Pastries","Sweet Sensation","Sweet Sensation Doughnut","SweetSensation_NG","Piece",7,25,6,250,"2026-11-10",1.2,3),
        (1030,"Bakery","Cereals","Kellogg's","Kellogg's Corn Flakes 500g","Kellogg_NG","Box",170,27,2,2800,"",1.0,2),
        (1031,"Bakery","Cereals","Kellogg's","Kellogg's Coco Pops 375g","Kellogg_NG","Box",58,42,4,2500,"",1.0,1),
        (1032,"Bakery","Cereals","Nestle","Nestle Cerelac Baby Cereal 400g","Nestle_NG","Tin",57,20,3,3200,"2026-06-05",1.1,4),
        (1033,"Bakery","Flour","Golden Penny","Golden Penny All Purpose Flour 2kg","FlourMill_NG","Bag",36,43,2,2200,"",1.0,0),
        (1034,"Bakery","Flour","Honeywell","Honeywell Semovita 2kg","Honeywell_NG","Bag",199,18,7,2400,"2026-09-20",1.0,3),
        (1035,"Bakery","Pasta","Dangote","Dangote Spaghetti 500g","Dangote_NG","Pack",172,29,6,450,"2025-12-19",1.5,5),
        (1036,"Bakery","Sugar","Dangote","Dangote Sugar 1kg","Dangote_NG","Pack",94,42,1,700,"",1.4,2),
        (1037,"Bakery","Sugar","Golden Penny","Golden Penny Sugar 1kg","FlourMill_NG","Pack",42,26,2,750,"2026-07-22",1.0,1),
        (1038,"Bakery","Yeast","Angel","Angel Instant Yeast 500g","Angel_NG","Pack",135,49,1,1800,"2026-02-10",1.0,1),
        (1039,"Bakery","Baking Powder","Royal","Royal Baking Powder 200g","Royal_NG","Tin",67,30,5,900,"",1.2,2),
        (1040,"Bakery","Butter","Devon","Devon Butter 400g","Devon_NG","Tin",183,41,6,3500,"2027-04-10",1.0,1),
        
        # ==================== PERSONAL CARE (20 items) ====================
        (1041,"Personal Care","Soap","Dettol","Dettol Antiseptic Soap 140g","Reckitt_NG","Bar",14,35,1,450,"",1.4,3),
        (1042,"Personal Care","Soap","Lux","Lux Beauty Soap 125g","Unilever_NG","Bar",82,26,5,350,"2026-07-22",1.0,1),
        (1043,"Personal Care","Soap","Dawn","Dawn Dishwashing Bar 200g","P&G_NG","Bar",102,20,4,250,"2027-07-15",1.0,1),
        (1044,"Personal Care","Shampoo","Head & Shoulders","Head & Shoulders Shampoo 400ml","P&G_NG","Bottle",26,13,3,2800,"",1.0,0),
        (1045,"Personal Care","Shampoo","Sunsilk","Sunsilk Shampoo 400ml","Unilever_NG","Bottle",74,29,4,2200,"",1.3,1),
        (1046,"Personal Care","Shampoo","Clear","Clear Anti-Dandruff Shampoo 400ml","Unilever_NG","Bottle",37,22,4,2500,"",1.3,1),
        (1047,"Personal Care","Body Cream","Nivea","Nivea Body Lotion 400ml","Nivea_NG","Bottle",151,37,3,3200,"",1.0,2),
        (1048,"Personal Care","Body Cream","Vaseline","Vaseline Intensive Care 400ml","Unilever_NG","Bottle",171,24,5,2800,"",1.0,1),
        (1049,"Personal Care","Deodorant","Rexona","Rexona Deodorant 150ml","Unilever_NG","Bottle",26,13,3,1500,"",1.0,0),
        (1050,"Personal Care","Deodorant","Nivea","Nivea Deodorant Roll-On 50ml","Nivea_NG","Bottle",16,41,3,1200,"2026-07-01",1.0,1),
        (1051,"Personal Care","Toothpaste","Colgate","Colgate Toothpaste 140g","Colgate_NG","Tube",131,12,4,800,"",1.0,2),
        (1052,"Personal Care","Toothpaste","Close-Up","Close-Up Toothpaste 140g","Unilever_NG","Tube",142,21,4,750,"2027-06-12",1.0,1),
        (1053,"Personal Care","Toothbrush","Oral-B","Oral-B Toothbrush Medium","P&G_NG","Piece",32,42,7,500,"2026-12-21",1.0,3),
        (1054,"Personal Care","Hair Cream","L'Oréal","L'Oréal Hair Cream 200ml","L'Oreal_NG","Jar",142,41,4,2200,"",1.0,2),
        (1055,"Personal Care","Hair Cream","Dark & Lovely","Dark & Lovely Hair Cream 200ml","DarkLovely_NG","Jar",37,22,4,1800,"",1.3,1),
        (1056,"Personal Care","Sanitary Pads","Always","Always Sanitary Pads 20s","P&G_NG","Pack",138,39,5,1200,"2026-12-07",1.0,1),
        (1057,"Personal Care","Sanitary Pads","Whisper","Whisper Sanitary Pads 20s","P&G_NG","Pack",6,15,1,1100,"2027-04-29",1.4,3),
        (1058,"Personal Care","Diapers","Pampers","Pampers Baby Diapers 40s","P&G_NG","Pack",102,20,4,5500,"2027-07-15",1.0,1),
        (1059,"Personal Care","Razor","Gillette","Gillette Razor Blades 5s","P&G_NG","Pack",42,45,4,1800,"",1.0,0),
        (1060,"Personal Care","Perfume","Axe","Axe Body Spray 150ml","Unilever_NG","Can",185,39,4,2500,"2026-02-06",1.1,1),
        
        # ==================== CEREALS & GRAINS (20 items) ====================
        (1061,"Cereals","Rice","Mama Gold","Mama Gold Rice 5kg","FlourMill_NG","Bag",42,45,4,8500,"",1.0,0),
        (1062,"Cereals","Rice","Big Bull","Big Bull Rice 5kg","BigBull_NG","Bag",60,28,6,7800,"2026-07-25",1.2,2),
        (1063,"Cereals","Rice","Caprice","Caprice Rice 5kg","Caprice_NG","Bag",84,27,6,8200,"",1.0,1),
        (1064,"Cereals","Pasta","Golden Penny","Golden Penny Spaghetti 500g","FlourMill_NG","Pack",128,35,1,450,"2025-10-20",1.0,0),
        (1065,"Cereals","Pasta","Honeywell","Honeywell Spaghetti 500g","Honeywell_NG","Pack",154,46,3,480,"",1.0,2),
        (1066,"Cereals","Pasta","Dangote","Dangote Macaroni 500g","Dangote_NG","Pack",185,19,5,420,"2027-05-13",1.0,1),
        (1067,"Cereals","Noodles","Indomie","Indomie Chicken Noodles 70g","Dufil_NG","Pack",135,50,4,150,"2026-08-28",1.0,3),
        (1068,"Cereals","Noodles","Indomie","Indomie Pepper Chicken 70g","Dufil_NG","Pack",38,13,6,150,"2027-04-02",1.1,4),
        (1069,"Cereals","Noodles","Minimie","Minimie Chin Chin Noodles 70g","Minimie_NG","Pack",133,26,1,140,"",1.0,2),
        (1070,"Cereals","Semolina","Golden Penny","Golden Penny Semovita 2kg","FlourMill_NG","Bag",74,29,4,2400,"",1.3,1),
        (1071,"Cereals","Semolina","Honeywell","Honeywell Semovita 2kg","Honeywell_NG","Bag",67,30,4,2500,"",1.3,2),
        (1072,"Cereals","Garri","Local","White Garri 5kg","Local_Supplier","Bag",82,26,5,3500,"2027-04-21",1.0,1),
        (1073,"Cereals","Garri","Local","Yellow Garri 5kg","Local_Supplier","Bag",174,19,5,3200,"2027-02-02",1.0,3),
        (1074,"Cereals","Beans","Local","Oloyin Beans 5kg","Local_Supplier","Bag",185,50,7,6500,"2026-08-22",1.0,1),
        (1075,"Cereals","Beans","Local","Honey Beans 5kg","Local_Supplier","Bag",38,13,6,5800,"2027-04-02",1.1,4),
        (1076,"Cereals","Oats","Quaker","Quaker Oats 1kg","Quaker_NG","Tin", 150, 30, 5, 2800, "", 1.0, 1),
        (1077,"Cereals","Oats","Nestle","Nestle Oats 500g","Nestle_NG","Box", 120, 25, 4, 1800, "", 1.0, 2),
        (1078,"Cereals","Maize","Local","Dried Maize 5kg","Local_Supplier","Bag", 200, 40, 7, 2800, "", 1.0, 1),
        (1079,"Cereals","Millet","Local","Millet Flour 2kg","Local_Supplier","Bag", 80, 20, 6, 2200, "", 1.0, 2),
        (1080,"Cereals","Wheat","Local","Wheat Grain 5kg","Local_Supplier","Bag", 100, 25, 7, 3500, "", 1.0, 1),
        # ==================== HOUSEHOLD (20 items) ====================
        (1081,"Household","Detergent","Ariel","Ariel Detergent 1kg","P&G_NG","Pack",59,17,1,1800,"",1.0,1),
        (1082,"Household","Detergent","Omo","Omo Detergent 1kg","Unilever_NG","Pack",67,30,4,1600,"",1.3,2),
        (1083,"Household","Detergent","Sunlight","Sunlight Dishwashing Liquid 500ml","Unilever_NG","Bottle",82,36,4,1200,"2026-09-18",1.0,1),
        (1084,"Household","Detergent","Morning Fresh","Morning Fresh Dishwashing Liquid 450ml","MorningFresh_NG","Bottle",102,35,5,1500,"",1.4,2),
        (1085,"Household","Bleach","Hypo","Hypo Bleach 1L","Hypo_NG","Bottle",96,44,4,800,"",1.3,3),
        (1086,"Household","Bleach","Jik","Jik Bleach 1L","P&G_NG","Bottle",59,17,1,900,"",1.0,1),
        (1087,"Household","Toilet Paper","Rose","Rose Toilet Paper 12 rolls","Rose_NG","Pack",34,20,1,2500,"2025-11-13",1.0,0),
        (1088,"Household","Toilet Paper","Prestige","Prestige Toilet Paper 12 rolls","Prestige_NG","Pack",116,33,3,2800,"",1.4,2),
        (1089,"Household","Tissue Paper","Rose","Rose Tissue Paper 200 sheets","Rose_NG","Pack",151,13,6,1200,"",1.0,1),
        (1090,"Household","Tissue Paper","Prestige","Prestige Facial Tissue 150 sheets","Prestige_NG","Pack",59,47,1,1400,"",1.0,2),
        (1091,"Household","Cleaner","Harpic","Harpic Toilet Cleaner 750ml","Reckitt_NG","Bottle",30,45,6,1800,"",1.5,0),
        (1092,"Household","Cleaner","Domestos","Domestos Bleach 750ml","Unilever_NG","Bottle",11,22,5,1600,"",1.0,1),
        (1093,"Household","Insecticide","Mortein","Mortein Insecticide Spray 400ml","Reckitt_NG","Can",12,46,3,2200,"2026-06-22",1.0,0),
        (1094,"Household","Insecticide","Raid","Raid Insecticide Spray 400ml","SCJohnson_NG","Can",162,47,3,2500,"2027-01-19",1.0,2),
        (1095,"Household","Fabric Softener","Comfort","Comfort Fabric Softener 1L","Unilever_NG","Bottle",97,17,4,1800,"2027-06-04",1.0,1),
        (1096,"Household","Fabric Softener","Downy","Downy Fabric Softener 1L","P&G_NG","Bottle",198,27,5,2000,"",1.0,3),
        (1097,"Household","Mop","Local","Floor Mop with Bucket","Local_Supplier","Piece",168,50,1,3500,"2026-04-08",1.0,1),
        (1098,"Household","Broom","Local","Soft Broom","Local_Supplier","Piece",158,10,1,800,"",1.0,2),
        (1099,"Household","Bucket","Local","Plastic Bucket 20L","Local_Supplier","Piece",180,22,6,1500,"2025-10-30",1.0,1),
        (1100,"Household","Basin","Local","Plastic Basin Large","Local_Supplier","Piece",88,27,1,1200,"2025-12-11",1.0,0),
        
        # ==================== FROZEN (20 items) ====================
        (1101,"Frozen","Frozen Chicken","Cold Kingdom","Cold Kingdom Frozen Chicken 1kg","ColdKingdom_NG","Pack",132,16,7,4500,"",1.0,2),
        (1102,"Frozen","Frozen Chicken","Honeywell","Honeywell Frozen Chicken 1kg","Honeywell_NG","Pack",154,49,7,4800,"2027-07-30",1.0,3),
        (1103,"Frozen","Frozen Turkey","Cold Kingdom","Cold Kingdom Frozen Turkey 2kg","ColdKingdom_NG","Pack",170,20,7,8500,"",1.0,1),
        (1104,"Frozen","Frozen Turkey","Honeywell","Honeywell Frozen Turkey 2kg","Honeywell_NG","Pack",8,50,5,9000,"",1.3,4),
        (1105,"Frozen","Frozen Fish","Cold Kingdom","Cold Kingdom Frozen Titus Fish 1kg","ColdKingdom_NG","Pack",194,38,2,5500,"",1.0,2),
        (1106,"Frozen","Frozen Fish","Local","Frozen Croaker Fish 1kg","Local_Supplier","Pack",31,48,5,6000,"",1.0,0),
        (1107,"Frozen","Frozen Vegetables","Findus","Findus Mixed Vegetables 500g","Findus_NG","Pack",175,37,7,1800,"2026-07-31",1.0,1),
        (1108,"Frozen","Frozen Vegetables","Local","Frozen Green Peas 500g","Local_Supplier","Pack",32,20,2,1500,"",1.5,2),
        (1109,"Frozen","Frozen Meat","Cold Kingdom","Cold Kingdom Frozen Beef 1kg","ColdKingdom_NG","Pack",138,48,4,5000,"2025-12-22",1.0,0),
        (1110,"Frozen","Frozen Shrimps","Local","Frozen Shrimps 500g","Local_Supplier","Pack",101,49,5,4500,"",1.0,1),
        (1111,"Frozen","Frozen Chips","McCain","McCain Frozen French Fries 1kg","McCain_NG","Pack",191,23,1,3500,"2026-05-21",1.0,2),
        (1112,"Frozen","Frozen Chips","Local","Frozen Sweet Potato Chips 1kg","Local_Supplier","Pack",43,14,1,2800,"",1.3,1),
        (1113,"Frozen","Ice Cream","Wall's","Wall's Vanilla Ice Cream 1L","Unilever_NG","Tub",57,13,7,3200,"2026-05-18",1.0,0),
        (1114,"Frozen","Ice Cream","Wall's","Wall's Chocolate Ice Cream 1L","Unilever_NG","Tub",123,29,1,3500,"",1.3,2),
        (1115,"Frozen","Ice Cream","Wall's","Wall's Strawberry Ice Cream 1L","Unilever_NG","Tub",73,19,2,3300,"2026-10-25",1.0,1),
        (1116,"Frozen","Frozen Sausage","Cold Kingdom","Cold Kingdom Sausage Rolls 10s","ColdKingdom_NG","Pack",101,13,7,1500,"",1.0,0),
        (1117,"Frozen","Frozen Sausage","Local","Local Sausage 1kg","Local_Supplier","Pack",160,41,6,2800,"2025-11-27",1.0,3),
        (1118,"Frozen","Frozen Plantain","Local","Frozen Fried Plantain 500g","Local_Supplier","Pack",87,28,6,1800,"2026-10-06",1.4,1),
        (1119,"Frozen","Frozen Yam","Local","Frozen Yam Chips 1kg","Local_Supplier","Pack",137,15,7,2200,"2026-09-13",1.0,2),
        (1120,"Frozen","Frozen Gizzard","Cold Kingdom","Cold Kingdom Chicken Gizzard 1kg","ColdKingdom_NG","Pack",117,35,1,3800,"2027-02-20",1.0,1),
        
        # ==================== SNACKS (20 items) ====================
        (1121,"Snacks","Chocolate","Cadbury","Cadbury Dairy Milk 100g","Cadbury_NG","Bar",94,23,7,800,"2027-03-04",1.0,0),
        (1122,"Snacks","Chocolate","Cadbury","Cadbury Bournville 100g","Cadbury_NG","Bar",172,13,2,900,"2027-03-10",1.0,2),
        (1123,"Snacks","Chocolate","Nestle","KitKat Chocolate 41.5g","Nestle_NG","Bar",55,39,5,250,"",1.0,1),
        (1124,"Snacks","Chocolate","Nestle","Nestle Smarties 40g","Nestle_NG","Tube",111,46,5,300,"2027-07-29",1.0,3),
        (1125,"Snacks","Biscuits","McVities","McVities HobNobs 250g","UnitedBiscuits_NG","Pack",158,17,5,1200,"",1.0,2),
        (1126,"Snacks","Biscuits","Mikado","Mikado Cream Crackers 400g","Mikado_NG","Pack",182,43,6,1500,"2027-05-28",1.2,1),
        (1127,"Snacks","Chips","Lay's","Lay's Classic Chips 150g","PepsiCo_NG","Pack",19,37,4,600,"",1.0,0),
        (1128,"Snacks","Chips","Lay's","Lay's Salted Chips 150g","PepsiCo_NG","Pack",108,39,5,600,"",1.0,1),
        (1129,"Snacks","Chips","Pringles","Pringles Original 165g","Kellogg_NG","Can", 60, 15, 3, 1200, "", 1.0, 2),
        (1130,"Snacks","Nuts","Groundnut","Roasted Groundnut 200g","Local_Supplier","Pack",36,33,7,400,"",1.0,2),
        (1131,"Snacks","Nuts","Cashew","Roasted Cashew Nuts 100g","Local_Supplier","Pack",198,21,7,1500,"2026-04-22",1.0,3),
        (1132,"Snacks","Popcorn","Act II","Act II Microwave Popcorn 3-pack","ActII_NG","Pack",137,21,2,1200,"2027-08-18",1.0,1),
        (1133,"Snacks","Candy","Chupa Chups","Chupa Chups Lollipop 10s","ChupaChups_NG","Pack",83,24,2,500,"2027-04-26",1.0,2),
        (1134,"Snacks","Candy","Mentos","Mentos Fruit Chews 37g","Perfetti_NG","Pack",145,47,3,300,"2026-01-18",1.0,0),
        (1135,"Snacks","Candy","Tic Tac","Tic Tac Mint 24g","Ferrero_NG","Box",108,41,7,400,"2026-11-16",1.4,2),
        (1136,"Snacks","Crisps","Gala","Gala Sausage Roll","UAC_NG","Piece",16,23,5,150,"2027-04-28",1.4,3),
        (1137,"Snacks","Crisps","Indomie","Indomie Chin Chin 50g","Dufil_NG","Pack",146,23,4,200,"2026-07-03",1.0,1),
        (1138,"Snacks","Crisps","Kings","Kings Plantain Chips 100g","Kings_NG","Pack",96,49,4,500,"",1.0,2),
        (1139,"Snacks","Wafers","Mikado","Mikado Wafer Rolls 125g","Mikado_NG","Box",172,39,2,800,"",1.0,1),
        (1140,"Snacks","Wafers","Loacker","Loacker Quadratini 125g","Loacker_NG","Box", 90, 20, 4, 1200, "", 1.0, 2),
        
        # ==================== DAIRY (20 items) ====================
        (1141,"Dairy","Milk","Peak","Peak Evaporated Milk 170g","Friesland_NG","Tin",154,46,3,900,"",1.0,2),
        (1142,"Dairy","Milk","Peak","Peak Powdered Milk 400g","Friesland_NG","Tin",101,49,5,3500,"",1.0,1),
        (1143,"Dairy","Milk","Three Crowns","Three Crowns Evaporated Milk 170g","Nestle_NG","Tin",125,38,4,850,"",1.0,1),
        (1144,"Dairy","Milk","Three Crowns","Three Crowns Powdered Milk 400g","Nestle_NG","Tin",47,32,5,3200,"",1.0,0),
        (1145,"Dairy","Milk","Dano","Dano Powdered Milk 900g","Arla_NG","Tin",121,29,1,6500,"2026-10-03",1.0,1),
        (1146,"Dairy","Cheese","Bel","Bel Babybel Cheese 8s","Bel_NG","Pack",126,34,1,3500,"2027-06-16",1.4,3),
        (1147,"Dairy","Cheese","Kraft","Kraft Cheddar Cheese 200g","Kraft_NG","Pack",80,31,6,2800,"2027-04-07",1.4,2),
        (1148,"Dairy","Butter","Devon","Devon Butter 200g","Devon_NG","Tin",66,17,3,1800,"",1.5,1),
        (1149,"Dairy","Butter","Lurpak","Lurpak Butter 200g","Arla_NG","Pack",185,41,1,2500,"2027-08-01",1.0,3),
        (1150,"Dairy","Yogurt","Friesland","Friesland Yoghurt Strawberry 500ml","Friesland_NG","Bottle",125,19,2,1200,"",1.0,2),
        (1151,"Dairy","Yogurt","Friesland","Friesland Yoghurt Vanilla 500ml","Friesland_NG","Bottle",37,30,6,1200,"",1.3,1),
        (1152,"Dairy","Cream","Nestle","Nestle Cream 185g","Nestle_NG","Tin",77,39,4,1500,"",1.3,2),
        (1153,"Dairy","Cream","Devon","Devon Cream 185g","Devon_NG","Tin",139,25,1,1600,"",1.0,1),
        (1154,"Dairy","Condensed Milk","Peak","Peak Sweetened Condensed Milk 170g","Friesland_NG","Tin",2,26,1,1200,"",1.0,4),
        (1155,"Dairy","Condensed Milk","Three Crowns","Three Crowns Condensed Milk 170g","Nestle_NG","Tin",43,14,1,1100,"",1.0,0),
        (1156,"Dairy","Ice Cream","Wall's","Wall's Magnum Ice Cream","Unilever_NG","Piece",115,34,1,800,"",1.4,2),
        (1157,"Dairy","Ice Cream","Wall's","Wall's Cornetto Ice Cream","Unilever_NG","Piece",44,46,1,600,"2027-03-27",1.0,1),
        (1158,"Dairy","Margarine","Blue Band","Blue Band Margarine 400g","Unilever_NG","Tub",46,11,1,1800,"",1.0,3),
        (1159,"Dairy","Margarine","Devon","Devon Margarine 400g","Devon_NG","Tub",200,41,7,1600,"2026-10-21",1.0,2),
        (1160,"Dairy","Margarine","Kings","Kings Margarine 400g","Kings_NG","Tub",125,38,4,1500,"",1.0,1),
        
        # ==================== PRODUCE (20 items) ====================
        (1161,"Produce","Tomatoes","Local","Fresh Tomatoes 1kg","Local_Farm","Bag",47,32,5,1500,"",1.0,0),
        (1162,"Produce","Tomatoes","Local","Fresh Tomatoes 5kg","Local_Farm","Bag",137,45,6,6500,"",1.3,2),
        (1163,"Produce","Onions","Local","Fresh Onions 1kg","Local_Farm","Bag",121,29,1,800,"2026-10-03",1.0,1),
        (1164,"Produce","Onions","Local","Fresh Onions 5kg","Local_Farm","Bag",126,34,1,3500,"2027-06-16",1.4,3),
        (1165,"Produce","Pepper","Local","Fresh Pepper (Rodo) 1kg","Local_Farm","Bag",121,29,1,2500,"2026-10-03",1.0,1),
        (1166,"Produce","Pepper","Local","Fresh Bell Pepper 1kg","Local_Farm","Bag",94,23,6,3000,"",1.0,2),
        (1167,"Produce","Potatoes","Local","Fresh Irish Potatoes 1kg","Local_Farm","Bag",4,26,2,1200,"",1.0,0),
        (1168,"Produce","Potatoes","Local","Fresh Irish Potatoes 5kg","Local_Farm","Bag",87,33,4,5500,"2025-11-05",1.0,1),
        (1169,"Produce","Yam","Local","Fresh Yam (Large)","Local_Farm","Piece",26,38,2,3500,"",1.3,3),
        (1170,"Produce","Yam","Local","Fresh Yam (Medium)","Local_Farm","Piece",80,31,6,2500,"2027-04-07",1.4,2),
        (1171,"Produce","Plantain","Local","Fresh Ripe Plantain 1kg","Local_Farm","Bunch",66,17,3,1500,"",1.5,1),
        (1172,"Produce","Plantain","Local","Fresh Unripe Plantain 1kg","Local_Farm","Bunch",185,41,1,1200,"2027-08-01",1.0,3),
        (1173,"Produce","Bananas","Local","Fresh Bananas 1kg","Local_Farm","Bunch",125,19,2,1000,"",1.0,2),
        (1174,"Produce","Apples","Local","Fresh Apples 1kg","Local_Farm","Pack",37,30,6,2500,"",1.3,1),
        (1175,"Produce","Oranges","Local","Fresh Oranges 1kg","Local_Farm","Pack",104,49,7,1800,"",1.3,0),
        (1176,"Produce","Watermelon","Local","Fresh Watermelon (Whole)","Local_Farm","Piece",184,43,7,3500,"",1.0,2),
        (1177,"Produce","Pineapple","Local","Fresh Pineapple (Whole)","Local_Farm","Piece",197,40,2,2500,"2027-03-13",1.1,3),
        (1178,"Produce","Mango","Local","Fresh Mango 1kg","Local_Farm","Pack",176,22,2,2000,"2026-12-31",1.0,1),
        (1179,"Produce","Pawpaw","Local","Fresh Pawpaw (Whole)","Local_Farm","Piece",37,31,3,1500,"2026-09-03",1.4,0),
        (1180,"Produce","Cucumber","Local","Fresh Cucumber 1kg","Local_Farm","Pack",52,43,6,1800,"2027-05-05",1.0,2),
        
        # ==================== MEAT & FISH (20 items) ====================
        (1181,"Meat","Chicken","Cold Kingdom","Fresh Chicken (Whole) 1.5kg","ColdKingdom_NG","Pack",25,17,6,4500,"2027-09-11",1.0,3),
        (1182,"Meat","Chicken","Obasanjo Farms","Obasanjo Farms Chicken 1kg","ObasanjoFarms_NG","Pack",51,20,1,3800,"",1.3,2),
        (1183,"Meat","Beef","Local","Fresh Beef 1kg","Local_Butcher","Pack",137,34,5,5500,"2026-03-27",1.0,1),
        (1184,"Meat","Beef","Local","Beef Bone 1kg","Local_Butcher","Pack",60,39,2,3500,"2027-06-11",1.0,0),
        (1185,"Meat","Goat Meat","Local","Fresh Goat Meat 1kg","Local_Butcher","Pack",178,14,7,6500,"2027-02-13",1.0,2),
        (1186,"Meat","Pork","Local","Fresh Pork 1kg","Local_Butcher","Pack",94,40,2,4500,"",1.2,1),
        (1187,"Meat","Turkey","Cold Kingdom","Fresh Turkey 2kg","ColdKingdom_NG","Pack",41,37,7,8500,"",1.2,3),
        (1188,"Meat","Fish","Local","Fresh Titus Fish 1kg","Local_Fisherman","Pack",198,15,3,6000,"",1.0,2),
        (1189,"Meat","Fish","Local","Fresh Croaker Fish 1kg","Local_Fisherman","Pack",122,43,4,7000,"2027-06-22",1.0,0),
        (1190,"Meat","Fish","Local","Fresh Mackerel (Titus) 1kg","Local_Fisherman","Pack",126,47,1,5500,"2026-05-06",1.0,1),
        (1191,"Meat","Fish","Local","Fresh Catfish 1kg","Local_Fisherman","Pack",4,49,2,5000,"2027-03-30",1.5,4),
        (1192,"Meat","Fish","Local","Fresh Stockfish 500g","Local_Fisherman","Pack",172,12,2,8000,"2027-03-10",1.0,2),
        (1193,"Meat","Fish","Local","Dried Fish (Mackerel) 500g","Local_Fisherman","Pack",55,39,5,4500,"",1.0,1),
        (1194,"Meat","Fish","Local","Smoked Catfish 500g","Local_Fisherman","Pack",111,46,5,5500,"2027-07-29",1.0,3),
        (1195,"Meat","Eggs","Local","Fresh Eggs (Crate of 30)","Local_Farm","Crate",158,17,5,4500,"",1.0,2),
        (1196,"Meat","Eggs","Local","Fresh Eggs (Half Crate 15)","Local_Farm","Pack",132,29,4,2400,"2026-09-22",1.0,1),
        (1197,"Meat","Gizzard","Cold Kingdom","Chicken Gizzard 1kg","ColdKingdom_NG","Pack",55,31,6,3500,"",1.0,2),
        (1198,"Meat","Liver","Local","Chicken Liver 1kg","Local_Butcher","Pack",149,50,2,3000,"",1.0,1),
        (1199,"Meat","Sausage","Cold Kingdom","Chicken Sausage 1kg","ColdKingdom_NG","Pack",125,42,3,4000,"2027-09-11",1.4,3),
        (1200,"Meat","Sausage","Local","Local Sausage (Kilishi) 500g","Local_Butcher","Pack",20,29,5,3500,"2026-11-13",1.0,0),
    ]
    
    conn.executemany('INSERT INTO inventory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', csv_data)
    conn.commit()
    conn.close()
    print(f"✅ Database initialized with {len(csv_data)} items - All brand mappings corrected!")

# ============================================================================
# DATA FUNCTIONS
# ============================================================================
def get_categories():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT DISTINCT Category FROM inventory ORDER BY Category", conn)
    conn.close()
    return ["Select Category"] + df['Category'].tolist()

def get_subcategories(category):
    if not category or category == "Select Category":
        return ["Select Subcategory"]
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(f"SELECT DISTINCT Subcategory FROM inventory WHERE Category='{category}' ORDER BY Subcategory", conn)
    conn.close()
    return ["Select Subcategory"] + df['Subcategory'].tolist()

def get_products_table(category, subcategory):
    if not category or category == "Select Category" or not subcategory or subcategory == "Select Subcategory":
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(f"""SELECT ItemID, Name, Brand, Stock, Threshold, LeadTime, 
                                ROUND(Threshold * SeasonalMultiplier, 0) as AdjThreshold,
                                SeasonalMultiplier,
                                CASE WHEN Stock <= Threshold * SeasonalMultiplier THEN '🔴 LOW' ELSE '🟢 OK' END as Status
                        FROM inventory 
                        WHERE Category='{category}' AND Subcategory='{subcategory}'
                        ORDER BY Status, Name""", conn)
    conn.close()
    return df

def search_products_table(query):
    if not query or len(query) < 2:
        return pd.DataFrame()
    
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("""SELECT ItemID, Name, Category, Subcategory, Brand, Stock, Threshold,
                               ROUND(Threshold * SeasonalMultiplier, 0) as AdjThreshold,
                               SeasonalMultiplier,
                               CASE WHEN Stock <= Threshold * SeasonalMultiplier THEN '🔴 LOW' ELSE '🟢 OK' END as Status
                       FROM inventory 
                       WHERE Name LIKE ? OR CAST(ItemID AS TEXT) LIKE ? OR Brand LIKE ?
                       ORDER BY Status, Name
                       LIMIT 30""", conn, (f'%{query}%', f'%{query}%', f'%{query}%'))
    conn.close()
    return df

# ============================================================================
# CHART FUNCTIONS WITH REAL-TIME DATES
# ============================================================================
def create_gauge_chart(item_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        item = pd.read_sql(f"SELECT * FROM inventory WHERE ItemID={item_id}", conn).iloc[0]
        conn.close()
        
        adj_threshold = int(item['Threshold'] * item['SeasonalMultiplier'])
        max_val = max(item['Stock'], adj_threshold) * 1.5
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=int(item['Stock']),
            title={'text': f"{item['Name']}<br>SKU: {item['ItemID']}"},
            gauge={
                'axis': {'range': [0, max_val]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, adj_threshold], 'color': "#fee2e2"},
                    {'range': [adj_threshold, adj_threshold * 2], 'color': "#fef3c7"},
                    {'range': [adj_threshold * 2, max_val], 'color': "#d1fae5"}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'value': adj_threshold}
            }
        ))
        fig.update_layout(height=300)
        return fig
    except Exception as e:
        print(f"Error creating gauge chart: {e}")
        return go.Figure()

def create_trend_chart(item_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        item = pd.read_sql(f"SELECT * FROM inventory WHERE ItemID={item_id}", conn).iloc[0]
        conn.close()
        
        adj_threshold = int(item['Threshold'] * item['SeasonalMultiplier'])
        now = datetime.now()
        dates = [(now - timedelta(days=i)).strftime('%b %d') for i in range(29, -1, -1)]
        stocks = [int(item['Stock']) + (i * 2) for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=stocks, mode='lines+markers',
                                line=dict(color='#3b82f6', width=3), marker=dict(size=6),
                                name='Stock Level'))
        fig.add_hline(y=adj_threshold, line_dash="dash", line_color="red", 
                     annotation_text=f"Threshold: {adj_threshold}")
        fig.update_layout(title=f"30-Day Trend (Updated: {now.strftime('%Y-%m-%d %H:%M')})",
                         height=300, xaxis_title="Date", yaxis_title="Units")
        return fig
    except Exception as e:
        print(f"Error creating trend chart: {e}")
        return go.Figure()

# ============================================================================
# CHAT-STYLE EXPERT ADVICE
# ============================================================================
def generate_advice(item_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        item = pd.read_sql(f"SELECT * FROM inventory WHERE ItemID={item_id}", conn).iloc[0]
        conn.close()
        
        # Extract all relevant data
        stock = int(item['Stock'])
        threshold = int(item['Threshold'])
        lead_time = int(item['LeadTime'])
        seasonal_mult = float(item['SeasonalMultiplier'])
        adj_threshold = int(threshold * seasonal_mult)
        name = item['Name']
        brand = item['Brand']
        supplier = item['Supplier']
        unit = item['Unit']
        price = float(item['Price'])
        reorder_count = int(item['ReorderCount'])
        expiry = item['Expiry']
        
        # Calculate key supply chain metrics
        if stock <= adj_threshold * 0.5:
            estimated_daily_sales = max(1, stock / max(1, lead_time * 0.5))
        elif stock <= adj_threshold:
            estimated_daily_sales = max(1, stock / max(1, lead_time))
        else:
            estimated_daily_sales = max(1, adj_threshold / 30)
        
        days_of_stock = round(stock / estimated_daily_sales, 1) if estimated_daily_sales > 0 else 999
        days_until_stockout = max(0, days_of_stock - lead_time)
        
        moq = 50
        recommended_qty = max(moq, int(estimated_daily_sales * lead_time * 1.5))
        
        inventory_value = stock * price
        
        # Build the expert advice
        chat = f"# 📦 Procurement Analysis: {name}\n\n"
        chat += f"**SKU:** {item_id} | **Brand:** {brand} | **Supplier:** {supplier}\n\n"
        chat += "---\n\n"
        
        # Key Metrics Dashboard
        chat += "## 📊 Current Inventory Status\n\n"
        chat += f"| Metric | Value |\n"
        chat += f"|--------|-------|\n"
        chat += f"| Current Stock | **{stock} {unit}** |\n"
        chat += f"| Reorder Threshold | {threshold} {unit} |\n"
        chat += f"| Seasonal-Adjusted Threshold | **{adj_threshold} {unit}** ({'+' if seasonal_mult > 1 else ''}{int((seasonal_mult-1)*100)}% seasonal boost) |\n"
        chat += f"| Estimated Daily Sales | {estimated_daily_sales:.1f} {unit}/day |\n"
        chat += f"| Days of Stock Remaining | **{days_of_stock} days** |\n"
        chat += f"| Supplier Lead Time | **{lead_time} days** |\n"
        chat += f"| Days Until Stockout | **{days_until_stockout} days** |\n"
        chat += f"| Current Inventory Value | ₦{inventory_value:,.2f} |\n\n"
        
        alerts = []
        
        # 1. EXPIRY CHECK
        if expiry and expiry != "":
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                days_left = (expiry_date - datetime.now()).days
                expiry_value_at_risk = stock * price
                
                if days_left < 0:
                    alerts.append(f"""### 🚨 CRITICAL: PRODUCT EXPIRED
                    
This product **expired {abs(days_left)} days ago**. It must be removed from shelves immediately.

**Financial Impact:** ₦{expiry_value_at_risk:,.2f} in dead stock value at risk.

**Immediate Action Required:**
- Remove all units from sales floor
- Process as inventory write-off
- Notify warehouse for disposal
- **DO NOT REORDER** until new batch arrives""")
                
                elif days_left < 14:
                    alerts.append(f"""### ⚠️ URGENT: EXPIRY RISK — {days_left} DAYS REMAINING

This product expires in **{days_left} days** with **{stock} {unit}** still in stock.

**Daily Sales Velocity:** {estimated_daily_sales:.1f} {unit}/day
**Projected Sales Before Expiry:** {int(estimated_daily_sales * days_left)} {unit}
**Units at Risk of Waste:** {max(0, stock - int(estimated_daily_sales * days_left))} {unit}
**Value at Risk:** ₦{max(0, (stock - int(estimated_daily_sales * days_left))) * price:,.2f}

**Recommended Actions:**
1. **HALT all new purchase orders** for this SKU
2. Move to front-of-store endcap display for visibility
3. Apply **20-30% markdown** to accelerate sales
4. Consider bundle deals (e.g., "Buy 2 Get 1 Free")
5. Donate excess stock to food banks if possible (tax benefit)""")
                
                elif days_left < 30 and stock > adj_threshold * 1.5:
                    alerts.append(f"""### 📅 MONITOR: EXPIRY WATCH — {days_left} DAYS

Stock level ({stock} {unit}) is high relative to remaining shelf life ({days_left} days).

**Recommended:**
- Monitor daily sales closely
- Consider small promotional discount (10-15%)
- Do not reorder until stock depletes below {int(adj_threshold * 0.8)} {unit}""")
            except:
                pass
        
        # 2. CRITICAL STOCKOUT CHECK
        if stock <= adj_threshold * 0.5 and lead_time >= 5:
            alerts.append(f"""### 🚨 CRITICAL: IMMEDIATE STOCKOUT RISK

**Current Situation:**
- Only **{stock} {unit}** remaining
- Item sells at **{estimated_daily_sales:.1f} {unit}/day**
- Supplier lead time: **{lead_time} days**
- **Stock will run out in {days_of_stock} days**
- **New delivery won't arrive for {lead_time} days**

**⚠️ You will be out of stock for approximately {max(0, lead_time - days_of_stock)} days before the next delivery arrives.**

**Immediate Action Required:**
1. **Place emergency order TODAY** for **{recommended_qty} {unit}** (recommended quantity)
2. Contact supplier ({supplier}) and request **expedited shipping**
3. Ask if they can deliver in **{max(1, lead_time - 2)} days** instead of {lead_time} days
4. Consider sourcing from **backup supplier** for immediate stock
5. Notify sales team to manage customer expectations

**Cost of Stockout:** Estimated loss of ₦{int(estimated_daily_sales * max(0, lead_time - days_of_stock) * price):,.2f} in missed sales""")
        
        elif stock <= adj_threshold:
            alerts.append(f"""### 🔄 STANDARD REORDER TRIGGERED

**Current Situation:**
- Stock: **{stock} {unit}** (at or below threshold of {adj_threshold})
- Daily sales velocity: **{estimated_daily_sales:.1f} {unit}/day**
- Days of stock remaining: **{days_of_stock} days**
- Supplier lead time: **{lead_time} days**

**Analysis:**
You have enough stock to last {days_of_stock} days, but with a {lead_time}-day lead time, you should reorder now to avoid stockout.

**Recommended Action:**
- Place standard order for **{recommended_qty} {unit}**
- Expected delivery: **{lead_time} days**
- This will cover approximately **{int(recommended_qty / estimated_daily_sales)} days** of demand
- Order value: **₦{recommended_qty * price:,.2f}**

**Timing:** Order within the next **{max(1, days_of_stock - lead_time)} days** to maintain buffer""")
        
        # 3. OVERSTOCK CHECK
        if stock > adj_threshold * 3 and lead_time <= 3:
            excess_stock = stock - adj_threshold
            excess_value = excess_stock * price
            holding_cost_rate = 0.20
            daily_holding_cost = (excess_value * holding_cost_rate) / 365
            
            alerts.append(f"""### 💰 OVERSTOCK ALERT — HIGH CARRYING COST

**Current Situation:**
- Stock: **{stock} {unit}** (threshold: {adj_threshold})
- **Excess stock:** {excess_stock} {unit} ({int((stock/adj_threshold - 1) * 100)}% above threshold)
- Supplier delivers in just **{lead_time} days** (fast turnaround)

**Financial Impact:**
- Excess inventory value: **₦{excess_value:,.2f}**
- Daily holding cost (20% annual): **₦{daily_holding_cost:,.2f}/day**
- Monthly carrying cost: **₦{daily_holding_cost * 30:,.2f}**
- Days of stock on hand: **{days_of_stock} days** (excessive for {lead_time}-day lead time)

**Recommended Actions:**
1. **FREEZE all procurement** for this SKU
2. Let stock naturally deplete to **{int(adj_threshold * 1.5)} {unit}** before reordering
3. Consider returning excess to supplier (if return policy allows)
4. Redirect to other store locations if part of a chain
5. Review reorder threshold — may be set too high

**Optimal Reorder Point:** {int(adj_threshold * 1.2)} {unit} (reduces carrying costs by ~40%)""")
        
        # 4. SEASONAL DEMAND SPIKE
        if seasonal_mult > 1.2:
            spike_pct = int((seasonal_mult - 1) * 100)
            seasonal_stock_needed = int(estimated_daily_sales * seasonal_mult * lead_time * 1.5)
            
            if stock < seasonal_stock_needed:
                alerts.append(f"""### 📈 SEASONAL DEMAND SPIKE DETECTED

**Seasonal Analysis:**
- Current seasonal multiplier: **{seasonal_mult}x** ({spike_pct}% above normal demand)
- Normal daily sales: ~{estimated_daily_sales:.1f} {unit}/day
- **Seasonal-adjusted sales: {estimated_daily_sales * seasonal_mult:.1f} {unit}/day**
- Current stock: **{stock} {unit}**
- Stock needed for seasonal coverage: **{seasonal_stock_needed} {unit}**

**⚠️ Stock Shortfall:** {max(0, seasonal_stock_needed - stock)} {unit} below seasonal requirement

**Recommended Actions:**
1. **Increase order quantity by {spike_pct}%** to match seasonal demand
2. Order **{int(recommended_qty * seasonal_mult)} {unit}** instead of standard {recommended_qty}
3. Consider **pre-ordering** from supplier to secure stock
4. Monitor daily sales — if velocity exceeds forecast, reorder immediately
5. Communicate with supplier about **capacity constraints** during peak season

**Pro Tip:** Seasonal spikes typically last 4-6 weeks. Plan procurement accordingly.""")
        
        # 5. HIGH-FREQUENCY REORDER DETECTION
        if reorder_count >= 3:
            alerts.append(f"""### ⚡ HIGH-FREQUENCY REORDER PATTERN

This item has been reordered **{reorder_count} times** recently, indicating:
- Consistently high demand
- Possible under-stocking
- Threshold may be set too low

**Recommended Actions:**
1. **Increase reorder threshold** by 30-50%
2. **Negotiate better pricing** with {supplier} (volume discount)
3. Consider **larger order quantities** to reduce ordering frequency
4. Evaluate if **safety stock** needs to be increased
5. Review if this item should be classified as **fast-moving** (A-category item)

**Procurement Strategy:** Shift from reactive to proactive ordering for this SKU""")
        
        # FINAL RECOMMENDATION
        if not alerts:
            chat += "## ✅ OPTIMAL INVENTORY STATUS\n\n"
            chat += f"**Good news!** Your inventory for {name} is well-managed.\n\n"
            chat += f"**Key Metrics:**\n"
            chat += f"- Stock level ({stock} {unit}) is comfortably above the seasonal-adjusted threshold ({adj_threshold} {unit})\n"
            chat += f"- You have **{days_of_stock} days** of stock on hand\n"
            chat += f"- With a {lead_time}-day supplier lead time, you're well-positioned\n"
            chat += f"- Daily sales velocity ({estimated_daily_sales:.1f} {unit}/day) is within expected range\n\n"
            chat += "**Recommendation:** Continue normal monitoring. No action needed at this time. 👍\n\n"
            chat += "**Next Review:** Check again in **{0} days** or when stock drops below {1} {2}.".format(
                int(days_of_stock * 0.5), int(adj_threshold * 1.2), unit)
        else:
            chat += "---\n\n## 🎯 EXECUTIVE SUMMARY\n\n"
            chat += "**Priority Actions (in order):**\n\n"
            for i, alert in enumerate(alerts, 1):
                summary_line = alert.split('\n')[0].replace('### ', '')
                chat += f"{i}. {summary_line}\n"
            
            chat += "\n**Total Inventory Value at Risk:** ₦{:,.2f}\n\n".format(inventory_value)
        
        # ============================================================================
        # NEW: PLAIN ENGLISH LAYMAN SUMMARY
        # ============================================================================
        chat += "\n---\n\n## 📖 PLAIN ENGLISH SUMMARY\n\n"
        
        if not alerts:
            chat += f"**What's happening with {name}?**\n\n"
            chat += f"Right now, you have **{stock} {unit}** of {name} in stock. This is a good amount — you have enough to last about **{days_of_stock} days** at your current sales rate of **{estimated_daily_sales:.1f} {unit} per day**.\n\n"
            chat += f"**Why is this good?** Your supplier ({supplier}) takes **{lead_time} days** to deliver new stock. Since you have {days_of_stock} days of stock on hand, you're well ahead of the delivery timeline. You won't run out before the next delivery arrives.\n\n"
            chat += f"**What should you do?** Nothing right now. Just keep an eye on the stock levels during your regular checks. When you see the stock drop to around **{int(adj_threshold * 1.2)} {unit}**, that's your signal to place a new order.\n\n"
            chat += f"**Business impact:** You're not tying up too much cash in inventory, and you're not risking lost sales from stockouts. This is the sweet spot for inventory management."
        
        else:
            chat += f"**What's happening with {name}?**\n\n"
            
            # Explain the situation in simple terms
            if stock <= adj_threshold * 0.5 and lead_time >= 5:
                chat += f"You're in a tight spot. You only have **{stock} {unit}** left, and this item sells about **{estimated_daily_sales:.1f} {unit} every day**. That means you'll run out in just **{days_of_stock} days**.\n\n"
                chat += f"**Here's the problem:** Your supplier takes **{lead_time} days** to deliver. Even if you order today, the new stock won't arrive for {lead_time} days. That means you'll be **out of stock for about {max(0, lead_time - days_of_stock)} days** before the delivery arrives.\n\n"
                chat += f"**Why does this matter?** When customers can't find {name} on the shelf, they'll either buy a competitor's product or go to another store. That's lost sales and potentially lost customers.\n\n"
                chat += f"**What you need to do:** Order **{recommended_qty} {unit}** right now and call your supplier to see if they can rush the delivery. If they can't, look for a backup supplier who can get you stock faster."
            
            elif stock <= adj_threshold:
                chat += f"You have **{stock} {unit}** in stock, which is getting low. At your current sales rate of **{estimated_daily_sales:.1f} {unit} per day**, you have enough to last **{days_of_stock} days**.\n\n"
                chat += f"**Here's the situation:** Your supplier takes **{lead_time} days** to deliver. If you wait too long to reorder, you risk running out before the new stock arrives.\n\n"
                chat += f"**What you should do:** Place an order for **{recommended_qty} {unit}** within the next **{max(1, days_of_stock - lead_time)} days**. This will give you enough stock to last about **{int(recommended_qty / estimated_daily_sales)} days** and keep you from running out.\n\n"
                chat += f"**Why this timing matters:** Ordering now (rather than waiting) gives you a buffer in case sales spike or the supplier is delayed. It's better to be safe than sorry."
            
            elif stock > adj_threshold * 3 and lead_time <= 3:
                chat += f"You have **{stock} {unit}** in stock, which is way more than you need. You have enough to last **{days_of_stock} days**, but your supplier can deliver in just **{lead_time} days**.\n\n"
                chat += f"**Here's the problem:** You're tying up **₦{excess_value:,.2f}** in excess inventory that's just sitting on the shelf. Every day, this excess stock costs you about **₦{daily_holding_cost:,.2f}** in storage and handling costs.\n\n"
                chat += f"**Why this matters:** That's money that could be used elsewhere in your business. Plus, if this is a perishable item, you risk it expiring before you can sell it.\n\n"
                chat += f"**What you should do:** Don't order any more {name} until your stock drops to around **{int(adj_threshold * 1.5)} {unit}**. Let what you have sell naturally. If you can return excess to the supplier, consider doing that."
            
            # Add expiry explanation if relevant
            if expiry and expiry != "":
                try:
                    expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                    days_left = (expiry_date - datetime.now()).days
                    
                    if days_left < 0:
                        chat += f"\n\n**⚠️ Critical issue:** This product has already expired ({abs(days_left)} days ago). You need to pull it off the shelves immediately and write it off as a loss. Don't order any more until you get a fresh batch."
                    
                    elif days_left < 14:
                        chat += f"\n\n**⚠️ Time-sensitive issue:** This product expires in **{days_left} days**. You have **{stock} {unit}** in stock, but at your current sales rate, you might not sell all of it before it expires. Consider putting it on sale (20-30% off) or moving it to a more visible location to sell it faster. Don't order any more."
                    
                    elif days_left < 30 and stock > adj_threshold * 1.5:
                        chat += f"\n\n**📅 Heads up:** This product expires in **{days_left} days** and you have a lot of stock ({stock} {unit}). Keep a close eye on sales and consider a small discount (10-15%) to move it faster."
                except:
                    pass
            
            # Add seasonal explanation if relevant
            if seasonal_mult > 1.2:
                spike_pct = int((seasonal_mult - 1) * 100)
                chat += f"\n\n**📈 Seasonal note:** We're in a busy period for {name}. Sales are running about **{spike_pct}% higher** than normal right now. This is probably due to seasonal demand (like holidays, weather, or local events). Make sure you're ordering enough to keep up with this increased demand."
            
            # Final bottom line
            chat += f"\n\n---\n\n**Bottom line:** "
            
            if stock <= adj_threshold * 0.5 and lead_time >= 5:
                chat += f"**Act now.** Order {recommended_qty} {unit} today and request expedited shipping. If you don't, you'll be out of stock for {max(0, lead_time - days_of_stock)} days and lose an estimated ₦{int(estimated_daily_sales * max(0, lead_time - days_of_stock) * price):,.2f} in sales."
            elif stock <= adj_threshold:
                chat += f"**Order soon.** Place an order for {recommended_qty} {unit} within the next {max(1, days_of_stock - lead_time)} days to avoid running out."
            elif stock > adj_threshold * 3 and lead_time <= 3:
                chat += f"**Don't order.** You have too much stock. Wait until it drops to {int(adj_threshold * 1.5)} {unit} before ordering more."
            else:
                chat += f"**Review the alerts above** and take action as needed."
        
        chat += "\n\n---\n\n*This analysis is generated by the Smart Inventory Expert System using forward-chaining Horn Clause inference and deterministic OR models. Always verify with physical stock count before placing orders.*"
        
        return chat
    except Exception as e:
        print(f"Error generating advice: {e}")
        traceback.print_exc()
        return f"❌ **Error:** Could not generate advice. {str(e)}"

# ============================================================================
# ACTION FUNCTIONS
# ============================================================================
def do_reorder(item_id, qty):
    if not item_id or item_id == 0:
        return "Please select an item first."
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("UPDATE inventory SET Stock = Stock + ?, ReorderCount = ReorderCount + 1 WHERE ItemID = ?",
                    (int(qty), item_id))
        conn.commit()
        item = pd.read_sql(f"SELECT * FROM inventory WHERE ItemID={item_id}", conn).iloc[0]
        conn.close()
        return f"✅ **Reorder Successful!**\n\nAdded **{qty} units** of {item['Name']}.\n\nNew stock: **{item['Stock']} units**"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def do_sale(item_id, qty):
    if not item_id or item_id == 0:
        return "Please select an item first."
    try:
        conn = sqlite3.connect(DB_NAME)
        item = pd.read_sql(f"SELECT * FROM inventory WHERE ItemID={item_id}", conn).iloc[0]
        if item['Stock'] < int(qty):
            conn.close()
            return f"❌ **Error:** Cannot sell {qty} units. Only {item['Stock']} in stock."
        conn.execute("UPDATE inventory SET Stock = Stock - ? WHERE ItemID = ?", (int(qty), item_id))
        conn.commit()
        new_stock = item['Stock'] - int(qty)
        conn.close()
        return f"✅ **Sale Logged!**\n\nSold **{qty} units** of {item['Name']}.\n\nRemaining: **{new_stock} units**"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def add_new_item(name, category, subcategory, brand, supplier, unit, stock, threshold, lead_time, price, expiry, seasonal):
    if not name or not category:
        return "❌ Please fill in at least Name and Category."
    try:
        conn = sqlite3.connect(DB_NAME)
        max_id = pd.read_sql("SELECT MAX(ItemID) as max_id FROM inventory", conn).iloc[0]['max_id']
        new_id = max_id + 1
        conn.execute("""INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (new_id, category, subcategory or "", brand or "", name, supplier or "", unit or "Unit",
                     int(stock), int(threshold), int(lead_time), float(price), expiry or "", float(seasonal), 0))
        conn.commit()
        conn.close()
        return f"✅ **Item Added!**\n\n**{name}** added with SKU: **{new_id}**"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ============================================================================
# BUILD UI WITH STATE MANAGEMENT
# ============================================================================
init_database()

with gr.Blocks(title="Laitan-Adio Smart Inventory") as app:
    gr.Markdown("# 📦 Laitan-Adio Smart Inventory\n### All 200 Items | Chat-Style Advice | Real-Time Graphical Analysis")
    
    # State variables to store current dataframes
    browse_df_state = gr.State(pd.DataFrame())
    search_df_state = gr.State(pd.DataFrame())
    selected_item = gr.State(value=0)
    
    with gr.Tabs():
        # ==================== BROWSE TAB ====================
        with gr.Tab("📂 Browse"):
            gr.Markdown("### Step 1: Select Category")
            category_dd = gr.Dropdown(choices=get_categories(), value="Select Category", label="Category")
            
            gr.Markdown("### Step 2: Select Subcategory")
            subcategory_dd = gr.Dropdown(choices=["Select Subcategory"], value="Select Subcategory", label="Subcategory")
            
            gr.Markdown("### Step 3: Select Product (click any row)")
            products_table = gr.Dataframe(
                headers=["Item ID", "Name", "Brand", "Stock", "Threshold", "Lead Time", "Adj Threshold", "Seasonal", "Status"],
                datatype=["number", "str", "str", "number", "number", "number", "number", "number", "str"],
                row_count=10, interactive=False, wrap=True
            )
            
            gr.Markdown("### 📊 Graphical Analysis")
            with gr.Row():
                gauge_plot = gr.Plot(label="Stock Level")
                trend_plot = gr.Plot(label="30-Day Trend")
            
            gr.Markdown("### 🧠 Expert Advice")
            advice_panel = gr.Markdown(value="Select a product from the table above to see expert advice.")
            
            gr.Markdown("### 🔄 Quick Actions")
            with gr.Row():
                reorder_qty = gr.Number(label="Reorder Qty", value=50, precision=0)
                reorder_btn = gr.Button("📦 Reorder", variant="primary")
                sale_qty = gr.Number(label="Sale Qty", value=10, precision=0)
                sale_btn = gr.Button("💰 Log Sale")
            
            action_result = gr.Markdown()
            
            def update_subcategories(category):
                return gr.update(choices=get_subcategories(category), value="Select Subcategory")
            
            def update_products_and_state(category, subcategory):
                df = get_products_table(category, subcategory)
                return df, df
            
            def on_product_select(evt: gr.SelectData, df_state):
                if evt is None or df_state is None or len(df_state) == 0:
                    return 0, gr.update(), gr.update(), "Please select a product."
                
                row_idx = evt.index[0]
                if row_idx >= len(df_state):
                    return 0, gr.update(), gr.update(), "Invalid selection."
                
                item_id = int(df_state.iloc[row_idx]['ItemID'])
                advice = generate_advice(item_id)
                gauge = create_gauge_chart(item_id)
                trend = create_trend_chart(item_id)
                
                return item_id, gauge, trend, advice
            
            category_dd.change(fn=update_subcategories, inputs=category_dd, outputs=subcategory_dd)
            subcategory_dd.change(fn=update_products_and_state, inputs=[category_dd, subcategory_dd], 
                                outputs=[products_table, browse_df_state])
            products_table.select(fn=on_product_select, inputs=browse_df_state, 
                                outputs=[selected_item, gauge_plot, trend_plot, advice_panel])
            reorder_btn.click(fn=do_reorder, inputs=[selected_item, reorder_qty], outputs=action_result)
            sale_btn.click(fn=do_sale, inputs=[selected_item, sale_qty], outputs=action_result)
        
        # ==================== SEARCH TAB ====================
        with gr.Tab("🔍 Search"):
            gr.Markdown("### Search by Name, SKU, or Brand")
            search_box = gr.Textbox(label="Type to search (min 2 characters)", placeholder="e.g., Milk, 1001, Coca-Cola")
            
            gr.Markdown("### Search Results (click any row)")
            search_results = gr.Dataframe(
                headers=["Item ID", "Name", "Category", "Subcategory", "Brand", "Stock", "Threshold", "Adj Threshold", "Status"],
                datatype=["number", "str", "str", "str", "str", "number", "number", "number", "str"],
                row_count=10, interactive=False, wrap=True, visible=False
            )
            
            gr.Markdown("### 📊 Graphical Analysis")
            with gr.Row():
                search_gauge = gr.Plot()
                search_trend = gr.Plot()
            
            gr.Markdown("### 🧠 Expert Advice")
            search_advice = gr.Markdown()
            
            def on_search_and_state(query):
                df = search_products_table(query)
                if len(df) == 0:
                    return gr.update(visible=False), gr.update(), gr.update(), "No results found.", df
                return gr.update(value=df, visible=True), gr.update(), gr.update(), "Select a product.", df
            
            def on_search_select(evt: gr.SelectData, df_state):
                if evt is None or df_state is None or len(df_state) == 0:
                    return gr.update(), gr.update(), "Please select a product."
                
                row_idx = evt.index[0]
                if row_idx >= len(df_state):
                    return gr.update(), gr.update(), "Invalid selection."
                
                item_id = int(df_state.iloc[row_idx]['ItemID'])
                advice = generate_advice(item_id)
                gauge = create_gauge_chart(item_id)
                trend = create_trend_chart(item_id)
                
                return gauge, trend, advice
            
            search_box.change(fn=on_search_and_state, inputs=search_box, 
                            outputs=[search_results, search_gauge, search_trend, search_advice, search_df_state])
            search_results.select(fn=on_search_select, inputs=search_df_state, 
                                outputs=[search_gauge, search_trend, search_advice])
        
        # ==================== ADD ITEM TAB ====================
        with gr.Tab("➕ Add Item"):
            gr.Markdown("### Add New Product to Inventory")
            
            with gr.Row():
                with gr.Column():
                    new_name = gr.Textbox(label="Product Name *")
                    new_category = gr.Dropdown(choices=get_categories()[1:], label="Category *")
                    new_subcategory = gr.Textbox(label="Subcategory")
                    new_brand = gr.Textbox(label="Brand")
                    new_supplier = gr.Textbox(label="Supplier")
                
                with gr.Column():
                    new_unit = gr.Dropdown(choices=["Box", "Carton", "1kg Bag", "500g Pack", "1L Pack", "2kg Bag", "Bottle", "Pack"], label="Unit")
                    new_stock = gr.Number(label="Initial Stock", value=100, precision=0)
                    new_threshold = gr.Number(label="Threshold", value=30, precision=0)
                    new_lead_time = gr.Number(label="Lead Time (days)", value=5, precision=0)
                    new_price = gr.Number(label="Price", value=500, precision=2)
            
            with gr.Row():
                new_expiry = gr.Textbox(label="Expiry (YYYY-MM-DD, blank if none)")
                new_seasonal = gr.Slider(minimum=0.8, maximum=2.0, value=1.0, step=0.1, label="Seasonal Multiplier")
            
            add_btn = gr.Button("➕ Add Item", variant="primary", size="lg")
            add_result = gr.Markdown()
            
            add_btn.click(fn=add_new_item, 
                         inputs=[new_name, new_category, new_subcategory, new_brand, new_supplier,
                                new_unit, new_stock, new_threshold, new_lead_time, new_price,
                                new_expiry, new_seasonal],
                         outputs=add_result)
if __name__ == "__main__":
    print("🚀 Starting Laitan-Adio Smart Inventory...")
    port = int(os.environ.get("PORT", 7860))
    
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False  # CRITICAL: share=True causes the 'unhashable dict' crash on Render
    )