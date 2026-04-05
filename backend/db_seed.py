import sqlite3
import os
from database import get_connection, create_tables

def seed():
    create_tables()
    conn = get_connection()
    cursor = conn.cursor()

    # ─────────────────────────────────────────
    # FIRST AID DATA — English
    # ─────────────────────────────────────────
    first_aid_en = [
        ('choking',
         '1. Ask if the person can cough or speak.\n'
         '2. If they cannot, stand behind them.\n'
         '3. Give 5 firm back blows between shoulder blades.\n'
         '4. Give 5 abdominal thrusts (Heimlich maneuver).\n'
         '5. Alternate back blows and thrusts until object is dislodged.\n'
         '6. If they become unconscious, begin CPR.\n'
         '7. Call emergency services immediately.',
         'en'),

        ('bleeding',
         '1. Put on gloves if available.\n'
         '2. Apply firm direct pressure using a clean cloth or bandage.\n'
         '3. Elevate the wound above the level of the heart.\n'
         '4. Do NOT remove the cloth if soaked — add more on top.\n'
         '5. Maintain pressure for at least 10 minutes without peeking.\n'
         '6. If bleeding does not stop, apply a tourniquet above the wound.\n'
         '7. Seek medical help immediately.',
         'en'),

        ('burn',
         '1. Remove the person from the heat source immediately.\n'
         '2. Cool the burn under cool (not ice cold) running water for 20 minutes.\n'
         '3. Do NOT use ice, butter, oil, or toothpaste on the burn.\n'
         '4. Remove rings, watches, or tight items near the burned area.\n'
         '5. Cover loosely with a sterile non-fluffy dressing.\n'
         '6. Do not pop any blisters.\n'
         '7. Seek medical help for burns larger than palm size.',
         'en'),

        ('fracture',
         '1. Do NOT try to straighten or move the broken bone.\n'
         '2. Immobilize the area using a splint, board, or folded newspaper.\n'
         '3. Wrap the splint with bandage but not too tight.\n'
         '4. Apply a cold pack wrapped in cloth to reduce swelling.\n'
         '5. Keep the person still and calm.\n'
         '6. Do not give food or water in case surgery is needed.\n'
         '7. Get medical attention as soon as possible.',
         'en'),

        ('heart attack',
         '1. Make the person sit or lie in a comfortable position.\n'
         '2. Loosen tight clothing around neck, chest, and waist.\n'
         '3. Give one aspirin (325 mg) to chew if not allergic.\n'
         '4. Keep the person calm and reassured.\n'
         '5. If unconscious and not breathing, begin CPR.\n'
         '6. CPR: 30 chest compressions, then 2 rescue breaths.\n'
         '7. Call emergency services immediately — do not drive them.',
         'en'),

        ('drowning',
         '1. Do NOT enter water unless trained — throw a rope or object instead.\n'
         '2. Once out of water, lay the person flat on their back.\n'
         '3. Check for breathing — look, listen, feel for 10 seconds.\n'
         '4. If not breathing, tilt head back and lift chin to open airway.\n'
         '5. Give 5 rescue breaths (mouth to mouth).\n'
         '6. Begin CPR: 30 chest compressions + 2 breaths.\n'
         '7. Continue until help arrives or person breathes on their own.',
         'en'),

        ('snake bite',
         '1. Move the person away from the snake calmly.\n'
         '2. Keep the person completely still — movement spreads venom faster.\n'
         '3. Position bitten limb BELOW heart level.\n'
         '4. Remove rings, watches, tight clothing near the bite.\n'
         '5. Do NOT cut the wound, suck out venom, or apply tourniquet.\n'
         '6. Do NOT apply ice or give alcohol.\n'
         '7. Take the person to hospital as fast as possible.',
         'en'),

        ('unconscious',
         '1. Tap shoulders firmly and shout their name.\n'
         '2. If no response, call for help immediately.\n'
         '3. Open airway: tilt head back, lift chin gently.\n'
         '4. Check for breathing for 10 seconds.\n'
         '5. If breathing: place in recovery position (on their side).\n'
         '6. If NOT breathing: start CPR immediately.\n'
         '7. CPR: 30 hard, fast chest compressions + 2 rescue breaths.',
         'en'),

        ('electric shock',
         '1. Do NOT touch the person while they are in contact with electricity.\n'
         '2. Turn off the power source at the main switch.\n'
         '3. If you cannot turn off power, push them away with dry wood.\n'
         '4. Once safe, check for breathing and pulse.\n'
         '5. If not breathing, begin CPR.\n'
         '6. Cover burns with a clean dry cloth.\n'
         '7. Call emergency services immediately.',
         'en'),

        ('heat stroke',
         '1. Move the person to a cool or shaded area immediately.\n'
         '2. Lay them down and elevate their legs slightly.\n'
         '3. Remove excess clothing.\n'
         '4. Cool them rapidly: wet cloths on neck, armpits, groin.\n'
         '5. Fan them or use air conditioning if available.\n'
         '6. Give cool water to drink ONLY if fully conscious.\n'
         '7. Call emergency services — heat stroke can be fatal.',
         'en'),
        
        ('dog bite',
         '1. Wash the wound with soap and running water for 10 minutes.\n'
         '2. Apply antiseptic like Dettol or Betadine.\n'
         '3. Cover with a clean bandage.\n'
         '4. Do NOT try to close the wound tightly.\n'
         '5. Get rabies vaccination within 24 hours.\n'
         '6. Go to hospital immediately.',
         'en'),

         ('seizure',
         '1. Clear the area around the person — remove hard objects.\n'
         '2. Do NOT hold the person down or put anything in their mouth.\n'
         '3. Gently turn them on their side to prevent choking.\n'
         '4. Cushion their head with something soft.\n'
         '5. Time the seizure — if over 5 minutes, call emergency services.\n'
         '6. Stay with them until fully conscious.',
         'en'),

        ('allergic reaction',
         '1. Identify and remove the allergen source if possible.\n'
         '2. If they have an EpiPen, help them use it on outer thigh.\n'
         '3. Make them sit upright if breathing is difficult.\n'
         '4. Lay them flat with legs raised if they feel faint.\n'
         '5. Do not give food, water, or oral medicine if struggling to swallow.\n'
         '6. Call emergency services immediately.',
         'en'),

        ('food poisoning',
         '1. Make the person rest and stay calm.\n'
         '2. Give small sips of water or ORS to prevent dehydration.\n'
         '3. Do NOT induce vomiting unless advised by a doctor.\n'
         '4. Avoid solid food until vomiting stops.\n'
         '5. Monitor for signs of severe dehydration: dry mouth, no urination.\n'
         '6. Seek medical help if symptoms last more than 24 hours.',
         'en'),
        
    ]

    # ─────────────────────────────────────────
    # FIRST AID DATA — Hindi
    # ─────────────────────────────────────────
    first_aid_hi = [
        ('दम घुटना',
         '1. पूछें क्या वे खांस या बोल सकते हैं।\n'
         '2. यदि नहीं, तो उनके पीछे खड़े हों।\n'
         '3. कंधे के ब्लेड के बीच 5 बार जोर से थपथपाएं।\n'
         '4. हेमलिच मैनुवर करें — 5 पेट धक्के दें।\n'
         '5. जब तक वस्तु न निकले दोहराएं।\n'
         '6. बेहोश होने पर CPR शुरू करें।\n'
         '7. तुरंत आपातकालीन सेवा बुलाएं।',
         'hi'),

        ('खून बहना',
         '1. साफ कपड़े से घाव पर सीधा दबाव डालें।\n'
         '2. घाव को दिल के स्तर से ऊपर उठाएं।\n'
         '3. कपड़ा भीग जाए तो ऊपर से और लगाएं, हटाएं नहीं।\n'
         '4. 10 मिनट तक बिना देखे दबाव बनाए रखें।\n'
         '5. खून न रुके तो घाव के ऊपर टर्निकेट लगाएं।\n'
         '6. तुरंत डॉक्टर के पास जाएं।',
         'hi'),

        ('जलना',
         '1. व्यक्ति को गर्मी के स्रोत से दूर करें।\n'
         '2. 20 मिनट तक ठंडे पानी से जले हुए भाग को ठंडा करें।\n'
         '3. बर्फ, मक्खन या तेल का उपयोग न करें।\n'
         '4. छाले न फोड़ें।\n'
         '5. साफ पट्टी से ढकें।\n'
         '6. बड़े जलने पर तुरंत अस्पताल जाएं।',
         'hi'),
    ]

    # ─────────────────────────────────────────
    # SHELTER DATA
    # ─────────────────────────────────────────
    shelters = [
        ('Government Relief Camp',  'Near District Collector Office', 'Solapur', 500,  17.6805, 75.9064),
        ('Zilla Parishad School',   'Station Road',                   'Solapur', 300,  17.6750, 75.9100),
        ('Community Hall',          'Panchavati Nagar',               'Solapur', 200,  17.6900, 75.9000),
        ('Municipal Corporation',   'Near Bus Stand',                 'Solapur', 400,  17.6720, 75.9150),
        ('Red Cross Centre',        'Dr. Ambedkar Road',              'Solapur', 150,  17.6830, 75.9080),
        ('Solapur Civil Hospital',  'Solapur-Pune Highway',           'Solapur', 600, 17.6901, 75.9102),
        ('Army Relief Camp',        'Cantonment Area',                'Solapur', 800, 17.6650, 75.9200),
        ('Shivaji Stadium Shelter', 'Near Railway Station',           'Solapur', 350, 17.6720, 75.9180),
    ]

    # ─────────────────────────────────────────
    # EVACUATION ROUTES
    # ─────────────────────────────────────────
    evacuation = [
        ('flood', 'Solapur',
         '1. Move to higher ground immediately — do not wait.\n'
         '2. Avoid walking through flowing water — 6 inches can knock you down.\n'
         '3. Do NOT cross bridges over fast-moving water.\n'
         '4. Head to Government Relief Camp near Collector Office, Solapur.\n'
         '5. Take emergency kit: water, torch, documents, medicine.\n'
         '6. Turn off electricity at the main switch before leaving.\n'
         '7. Do not return home until authorities declare it safe.',
         'en'),

        ('earthquake', 'Solapur',
         '1. DROP to the ground immediately.\n'
         '2. Take COVER under a sturdy table or against an interior wall.\n'
         '3. HOLD ON and protect your head and neck with your arms.\n'
         '4. Stay away from windows, mirrors, and heavy furniture.\n'
         '5. Do NOT run outside during shaking — most injuries occur then.\n'
         '6. After shaking stops, exit building carefully.\n'
         '7. Move to open ground away from buildings and power lines.',
         'en'),

        ('fire', 'Solapur',
         '1. Shout FIRE loudly and activate the nearest fire alarm.\n'
         '2. Crawl low under smoke — clean air is near the floor.\n'
         '3. Feel every door with the back of your hand before opening.\n'
         '4. If door is hot, do NOT open it — use another exit.\n'
         '5. Use stairs only — NEVER use elevators during a fire.\n'
         '6. Once outside, move to the assembly point and do not re-enter.\n'
         '7. Call fire services: 101.',
         'en'),

        ('flood', 'Solapur',
         '1. तुरंत ऊंचे स्थान पर जाएं।\n'
         '2. बहते पानी में न चलें।\n'
         '3. पुलों को पार न करें।\n'
         '4. जिला कलेक्टर कार्यालय के पास राहत शिविर जाएं।\n'
         '5. जाने से पहले बिजली का मुख्य स्विच बंद करें।',
         'hi'),
        
        # ── ADD NEW EVACUATION ROUTES HERE ──
        ('cyclone', 'Solapur',
         '1. Listen to weather alerts on radio or local announcements.\n'
         '2. Move away from coastal or low-lying areas immediately.\n'
         '3. Secure or bring inside any loose outdoor objects.\n'
         '4. Close all windows and doors firmly.\n'
         '5. Go to the nearest government shelter.\n'
         '6. Do not go outside during peak cyclone winds.\n'
         '7. Wait for official all-clear before returning home.',
         'en'),

        ('gas leak', 'Solapur',
        '1. Do NOT switch any lights or electrical switches on or off.\n'
        '2. Do NOT use your phone inside the building.\n'
        '3. Open all windows and doors immediately.\n'
        '4. Turn off the gas valve at the cylinder or meter.\n'
        '5. Evacuate everyone from the building quickly.\n'
        '6. Call fire services from outside: 101.\n'
        '7. Do not re-enter until authorities confirm it is safe.',
        'en'),
    ]

    # Insert all data (ignore if already exists)
    cursor.executemany(
        'INSERT OR IGNORE INTO first_aid (condition, steps, language) VALUES (?, ?, ?)',
        first_aid_en + first_aid_hi
    )
    cursor.executemany(
        'INSERT OR IGNORE INTO shelters (name, address, city, capacity, lat, lng) VALUES (?, ?, ?, ?, ?, ?)',
        shelters
    )
    cursor.executemany(
        'INSERT OR IGNORE INTO evacuation_routes (disaster_type, region, instructions, language) VALUES (?, ?, ?, ?)',
        evacuation
    )

    conn.commit()
    conn.close()
    print(f"Database seeded successfully at: emergency.db")
    print(f"  First aid entries: {len(first_aid_en) + len(first_aid_hi)}")
    print(f"  Shelters: {len(shelters)}")
    print(f"  Evacuation routes: {len(evacuation)}")

if __name__ == '__main__':
    seed()
    print("Database seeded successfully!")