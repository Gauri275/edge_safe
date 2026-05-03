import sqlite3
import os
from database import get_connection, create_tables


def seed():
    create_tables()   # ← create tables FIRST

    # Now safe to delete old data
    conn = get_connection()
    conn.execute('DELETE FROM first_aid')
    conn.execute('DELETE FROM shelters')
    conn.execute('DELETE FROM evacuation_routes')
    conn.execute('DELETE FROM disaster_prone_areas')
    conn.commit()
    conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    # ... rest of your code continues here



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
        
        ('landslide',
        '1. Move away from the slide area immediately — go sideways not uphill.\n'
        '2. If escape is not possible, curl into a tight ball and protect your head.\n'
        '3. After the slide stops, watch out for broken gas lines and damaged power lines.\n'
        '4. Do not enter the slide area — secondary slides are common.\n'
        '5. Check for injured people nearby without entering unstable zones.\n'
        '6. Call emergency services: 112.\n'
        '7. Wait for NDRF and rescue teams before re-entering any area.',
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
    # FIRST AID DATA — Malayalam
    # ─────────────────────────────────────────
    
    # ── FIRST AID — Malayalam ──
    first_aid_ml = [
        ('ശ്വാസം മുട്ടൽ',
        '1. ചുമയ്ക്കാൻ കഴിയുമോ എന്ന് ചോദിക്കുക.\n'
        '2. പുറകിൽ നിന്ന് 5 തവണ ശക്തമായി തട്ടുക.\n'
        '3. ഹൈംലിക് മാനുവർ ചെയ്യുക.\n'
        '4. വസ്തു പുറത്തു വരുന്നത് വരെ ആവർത്തിക്കുക.\n'
        '5. അബോധാവസ്ഥയിലായാൽ CPR ആരംഭിക്കുക.',
        'ml'),

        ('രക്തസ്രാവം',
        '1. വൃത്തിയുള്ള തുണി കൊണ്ട് നേരിട്ട് സമ്മർദ്ദം ചെലുത്തുക.\n'
        '2. മുറിവ് ഹൃദയ നിരപ്പിന് മുകളിൽ ഉയർത്തുക.\n'
        '3. തുണി നനഞ്ഞാൽ അതിന്മേൽ കൂടുതൽ വയ്ക്കുക, നീക്കരുത്.\n'
        '4. 10 മിനിറ്റ് സമ്മർദ്ദം നിലനിർത്തുക.\n'
        '5. ഉടൻ ഡോക്ടറെ കാണുക.',
        'ml'),

        ('പൊള്ളൽ',
        '1. ചൂട് സ്രോതസ്സിൽ നിന്ന് ഉടൻ മാറ്റുക.\n'
        '2. 20 മിനിറ്റ് തണുത്ത വെള്ളം ഒഴിക്കുക.\n'
        '3. മഞ്ഞ്, വെണ്ണ, എണ്ണ ഉപയോഗിക്കരുത്.\n'
        '4. ശുദ്ധമായ വസ്ത്രം കൊണ്ട് മൂടുക.\n'
        '5. വലിയ പൊള്ളലിന് ഉടൻ ആശുപത്രിയിൽ പോകുക.',
        'ml'),
        
        ('മണ്ണിടിച്ചിൽ',
        '1. ഉടൻ സ്ലൈഡ് ഏരിയയിൽ നിന്ന് വശത്തേക്ക് മാറുക.\n'
        '2. രക്ഷപ്പെടാൻ കഴിയില്ലെങ്കിൽ തലയ്ക്ക് കൈ കൊണ്ട് മൂടി ഒതുങ്ങുക.\n'
        '3. സ്ലൈഡ് നിർത്തിയ ശേഷം ഗ്യാസ് ലൈൻ, വൈദ്യുതി തന്ത്രങ്ങൾ ശ്രദ്ധിക്കുക.\n'
        '4. NDRF ടീം വരും വരെ ഉരുൾ പ്രദേശത്ത് കയറരുത്.\n'
        '5. അടിയന്തര സേവനം: 112 വിളിക്കുക.',
        'ml'),
    ]
    
    # ── Tamil ──
    first_aid_ta = [
        ('மூச்சுத் திணறல்',
        '1. இருமல் முடியுமா என்று கேளுங்கள்.\n'
        '2. முதுகில் 5 முறை தட்டுங்கள்.\n'
        '3. வயிற்றை 5 முறை அழுத்துங்கள்.\n'
        '4. பொருள் வெளியே வரும் வரை தொடருங்கள்.\n'
        '5. மயக்கம் வந்தால் CPR தொடங்குங்கள்.',
        'ta'),
        ('இரத்தப்போக்கு',
        '1. சுத்தமான துணியால் நேரடியாக அழுத்துங்கள்.\n'
        '2. காயத்தை இதயத்திற்கு மேலே உயர்த்துங்கள்.\n'
        '3. துணி நனைந்தால் மேலே மேலும் வையுங்கள்.\n'
        '4. 10 நிமிடம் அழுத்தத்தை தொடருங்கள்.\n'
        '5. உடனே மருத்துவரை அணுகுங்கள்.',
        'ta'),
        ('தீக்காயம்',
        '1. உடனே வெப்ப மூலத்திலிருந்து விலகுங்கள்.\n'
        '2. 20 நிமிடம் குளிர்ந்த நீரில் வையுங்கள்.\n'
        '3.얼음, வெண்ணெய் பயன்படுத்தாதீர்கள்.\n'
        '4. சுத்தமான துணியால் மூடுங்கள்.\n'
        '5. பெரிய காயமாக இருந்தால் மருத்துவமனை செல்லுங்கள்.',
        'ta'),
    ]

    # ── Telugu ──
    first_aid_te = [
        ('శ్వాస ఆగిపోవడం',
        '1. దగ్గు వేయగలరా అని అడగండి.\n'
        '2. వీపుపై 5 సార్లు గట్టిగా కొట్టండి.\n'
        '3. పొట్టను 5 సార్లు నొక్కండి.\n'
        '4. వస్తువు బయటకు వచ్చే వరకు కొనసాగించండి.\n'
        '5. స్పృహ తప్పితే CPR ప్రారంభించండి.',
        'te'),
        ('రక్తస్రావం',
        '1. శుభ్రమైన గుడ్డతో నేరుగా ఒత్తిడి వేయండి.\n'
        '2. గాయాన్ని హృదయం కంటే పైకి లేపండి.\n'
        '3. గుడ్డ తడిస్తే పైన మరొకటి వేయండి.\n'
        '4. 10 నిమిషాలు ఒత్తిడి కొనసాగించండి.\n'
        '5. వెంటనే వైద్యుని వద్దకు వెళ్ళండి.',
        'te'),
        ('కాలిన గాయం',
        '1. వేడి మూలం నుండి వెంటనే దూరంగా వెళ్ళండి.\n'
        '2. 20 నిమిషాలు చల్లని నీటిలో పెట్టండి.\n'
        '3. మంచు, వెన్న వాడవద్దు.\n'
        '4. శుభ్రమైన గుడ్డతో కప్పండి.\n'
        '5. పెద్ద గాయమైతే వెంటనే ఆసుపత్రికి వెళ్ళండి.',
        'te'),
    ]

    # ── Kannada ──
    first_aid_kn = [
        ('ಉಸಿರುಗಟ್ಟುವಿಕೆ',
        '1. ಕೆಮ್ಮಲು ಸಾಧ್ಯವೇ ಎಂದು ಕೇಳಿ.\n'
        '2. ಬೆನ್ನಿನ ಮೇಲೆ 5 ಬಾರಿ ಜೋರಾಗಿ ತಟ್ಟಿ.\n'
        '3. ಹೊಟ್ಟೆಯನ್ನು 5 ಬಾರಿ ಒತ್ತಿ.\n'
        '4. ವಸ್ತು ಹೊರಬರುವವರೆಗೂ ಮುಂದುವರಿಸಿ.\n'
        '5. ಪ್ರಜ್ಞೆ ತಪ್ಪಿದರೆ CPR ಪ್ರಾರಂಭಿಸಿ.',
        'kn'),
        ('ರಕ್ತಸ್ರಾವ',
        '1. ಸ್ವಚ್ಛ ಬಟ್ಟೆಯಿಂದ ನೇರವಾಗಿ ಒತ್ತಡ ಹಾಕಿ.\n'
        '2. ಗಾಯವನ್ನು ಹೃದಯಕ್ಕಿಂತ ಮೇಲೆ ಎತ್ತಿ ಹಿಡಿಯಿರಿ.\n'
        '3. ಬಟ್ಟೆ ನೆನೆದರೆ ಮೇಲೆ ಇನ್ನೊಂದು ಹಾಕಿ.\n'
        '4. 10 ನಿಮಿಷ ಒತ್ತಡ ಮುಂದುವರಿಸಿ.\n'
        '5. ತಕ್ಷಣ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.',
        'kn'),
        ('ಬೆಂಕಿ ಸುಟ್ಟ ಗಾಯ',
        '1. ತಕ್ಷಣ ಬಿಸಿ ಮೂಲದಿಂದ ದೂರ ಸರಿಯಿರಿ.\n'
        '2. 20 ನಿಮಿಷ ತಣ್ಣೀರಿನಲ್ಲಿ ಇಡಿ.\n'
        '3. ಮಂಜುಗಡ್ಡೆ, ಬೆಣ್ಣೆ ಬಳಸಬೇಡಿ.\n'
        '4. ಸ್ವಚ್ಛ ಬಟ್ಟೆಯಿಂದ ಮುಚ್ಚಿ.\n'
        '5. ದೊಡ್ಡ ಗಾಯವಾದರೆ ಆಸ್ಪತ್ರೆಗೆ ಹೋಗಿ.',
        'kn'),
    ]
    
    

    # ─────────────────────────────────────────
    # SHELTER DATA
    # ─────────────────────────────────────────
    shelters = [
        # ── Mumbai ──
        ('Azad Maidan Relief Camp',       'Azad Maidan, Fort',           'Mumbai',    800, 18.9437, 72.8353),
        ('BKC Emergency Shelter',         'Bandra Kurla Complex',        'Mumbai',    600, 19.0596, 72.8656),
        ('Dharavi Community Hall',        'Dharavi Main Road',           'Mumbai',    400, 19.0400, 72.8557),

        # ── Pune ──
        ('Shivajinagar Relief Centre',    'Shivajinagar Bus Stand Road', 'Pune',      500, 18.5308, 73.8474),
        ('Hadapsar Emergency Camp',       'Hadapsar Industrial Area',    'Pune',      350, 18.5018, 73.9252),
        ('Katraj Shelter Point',          'Katraj Chowk',                'Pune',      300, 18.4529, 73.8654),

        # ── Nashik ──
        ('Nashik District Relief Camp',   'Near Collector Office',       'Nashik',    500, 20.0059, 73.7897),
        ('CBS Emergency Shelter',         'CBS Chowk',                   'Nashik',    300, 19.9975, 73.7898),
        ('Panchavati Community Centre',   'Panchavati Road',             'Nashik',    200, 20.0200, 73.7950),

        # ── Nagpur ──
        ('Civil Lines Relief Camp',       'Civil Lines Area',            'Nagpur',    600, 21.1498, 79.0806),
        ('Sitabuldi Emergency Centre',    'Sitabuldi Fort Road',         'Nagpur',    400, 21.1461, 79.0850),
        ('Nagpur Municipal Shelter',      'Gandhi Sagar Road',           'Nagpur',    300, 21.1523, 79.0762),

        # ── Solapur ──
        ('Government Relief Camp',        'Near District Collector',     'Solapur',   500, 17.6805, 75.9064),
        ('Zilla Parishad School',         'Station Road',                'Solapur',   300, 17.6750, 75.9100),
        ('Community Hall Shelter',        'Panchavati Nagar',            'Solapur',   200, 17.6900, 75.9000),
        ('Municipal Corporation Camp',    'Near Bus Stand',              'Solapur',   400, 17.6720, 75.9150),
        ('Red Cross Centre',              'Dr. Ambedkar Road',           'Solapur',   150, 17.6830, 75.9080),

        # ── Aurangabad (Chhatrapati Sambhajinagar) ──
        ('Aurangabad Relief Centre',      'Near Collector Office',       'Aurangabad',500, 19.8762, 75.3433),
        ('CIDCO Emergency Shelter',       'CIDCO Colony N-6',            'Aurangabad',350, 19.8716, 75.3278),

        # ── Kolhapur ──
        ('Rajaram College Ground Camp',   'Rajaram Road',                'Kolhapur',  600, 16.7050, 74.2433),
        ('Tarabai Park Relief Centre',    'Tarabai Park Road',           'Kolhapur',  400, 16.7167, 74.2333),

        # ── Nanded ──
        ('Nanded District Camp',          'Near SP Office',              'Nanded',    400, 19.1383, 77.3210),
        ('Guru Nanak Mission Shelter',    'Hazur Sahib Road',            'Nanded',    300, 19.1530, 77.3175),

        # ── Latur ──
        ('Latur Relief Camp',             'Near Collectorate',           'Latur',     450, 18.4088, 76.5604),
        ('Udgir Road Emergency Shelter',  'Udgir Road',                  'Latur',     250, 18.4000, 76.5700),

        # ── Hyderabad ──
        ('LB Stadium Relief Camp',        'LB Stadium, Basheerbagh',     'Hyderabad', 800, 17.3962, 78.4700),
        ('Nampally Emergency Centre',     'Nampally Station Road',       'Hyderabad', 500, 17.3840, 78.4742),

        # ── Bangalore ──
        ('Cubbon Park Relief Camp',       'Cubbon Park Main Gate',       'Bangalore', 700, 12.9763, 77.5929),
        ('Koramangala Emergency Shelter', 'Koramangala 4th Block',       'Bangalore', 400, 12.9352, 77.6245),

        # ── Chennai ──
        ('Marina Beach Relief Camp',      'Marina Beach Road',           'Chennai',   900, 13.0500, 80.2824),
        ('Egmore Emergency Shelter',      'Egmore Station Road',         'Chennai',   500, 13.0785, 80.2615),

        # ── Kochi ──
        ('Ernakulam Relief Centre',       'MG Road, Ernakulam',          'Kochi',     600, 9.9816,  76.2999),
        ('Fort Kochi Emergency Shelter',  'Fort Kochi Beach Road',       'Kochi',     300, 9.9658,  76.2421),

        # ── Delhi ──
        ('Ramlila Ground Camp',           'Ramlila Ground, Old Delhi',   'Delhi',    1200, 28.6445, 77.2345),
        ('Yamuna Relief Centre',          'Yamuna Ghat Road',            'Delhi',     800, 28.6562, 77.2410),
        
        #Sshelters = 
        # ... existing cities ...

        # ── Wayanad ──   ← must be inside this list
        ('Kalpetta Government College Camp',  'Kalpetta Town',              'Wayanad', 600, 11.6074, 76.0821),
        ('Mananthavady Relief Centre',        'Mananthavady Town Centre',   'Wayanad', 400, 11.8007, 76.0012),
        ('Sulthan Bathery Camp',              'Near Bathery Bus Stand',     'Wayanad', 350, 11.6483, 76.2614),
        ('Ambalavayal Tribal Shelter',        'Ambalavayal Village Road',   'Wayanad', 200, 11.6833, 76.1667),
        ('Vythiri Community Hall',            'Vythiri Junction',           'Wayanad', 250, 11.5667, 76.0167),
        ('Padinharathara Relief Camp',        'Padinharathara Panchayath',  'Wayanad', 180, 11.5833, 76.0500),
        ('Meppadi Emergency Shelter',         'Meppadi Town',               'Wayanad', 300, 11.5167, 76.1000),
        ('Kalpetta District Hospital Camp',   'District Hospital Road',     'Wayanad', 150, 11.6090, 76.0833),
    
    ]

    # ─────────────────────────────────────────
    # EVACUATION ROUTES
    # ─────────────────────────────────────────
    evacuation = [
        # ── FLOOD — English ──
        ('flood', 'Mumbai',
        '1. Move immediately to higher ground — do not wait.\n'
        '2. Avoid Mithi River banks, low-lying areas of Kurla, Sion, Dharavi.\n'
        '3. Do NOT cross bridges over fast-moving water.\n'
        '4. Head to nearest relief camp: Azad Maidan or BKC.\n'
        '5. Turn off electricity at main switch before leaving.\n'
        '6. Take emergency kit: water, torch, documents, medicines.\n'
        '7. Do not return home until authorities declare it safe.',
        'en'),

        ('flood', 'Pune',
        '1. Move away from Mula-Mutha River banks immediately.\n'
        '2. Avoid areas near Sangam Bridge and Holkar Bridge.\n'
        '3. Head to Shivajinagar Relief Centre or Hadapsar Emergency Camp.\n'
        '4. Do not drive through waterlogged underpasses.\n'
        '5. Turn off electricity before evacuating.\n'
        '6. Follow NDRF and PMC announcements on loudspeakers.\n'
        '7. Keep important documents in a waterproof bag.',
        'en'),

        ('flood', 'Nashik',
        '1. Move away from Godavari River banks immediately.\n'
        '2. Avoid Panchavati, Gangapur Road low-lying areas.\n'
        '3. Head to Nashik District Relief Camp near Collector Office.\n'
        '4. Do NOT attempt to cross flooded roads.\n'
        '5. Carry drinking water and first aid kit.\n'
        '6. Assist elderly and disabled neighbours to evacuate.\n'
        '7. Wait for official all-clear before returning.',
        'en'),

        ('flood', 'Kolhapur',
        '1. Move away from Panchaganga River banks immediately.\n'
        '2. Avoid Rajaram Bridge area and Kasaba Bawada zone.\n'
        '3. Head to Rajaram College Ground Camp.\n'
        '4. Do not enter floodwater — even 6 inches can be dangerous.\n'
        '5. Follow Kolhapur Municipal Corporation announcements.\n'
        '6. Turn off gas and electricity before leaving.\n'
        '7. Keep emergency contact numbers saved offline.',
        'en'),

        ('flood', 'Hyderabad',
        '1. Move away from Musi River and Hussain Sagar lake area.\n'
        '2. Avoid low-lying areas of Toli Chowki, Moosarambagh.\n'
        '3. Head to LB Stadium Relief Camp, Basheerbagh.\n'
        '4. Do not use underpasses or subways during heavy rain.\n'
        '5. Follow GHMC and NDRF instructions.\n'
        '6. Keep vehicles on high ground to avoid waterlogging.\n'
        '7. Do not touch electric poles or wires in floodwater.',
        'en'),

        ('flood', 'Kochi',
        '1. Move away from backwaters and low-lying coastal areas.\n'
        '2. Avoid Aluva, Perumbavoor, and Chalakudy riverside zones.\n'
        '3. Head to Ernakulam Relief Centre on MG Road.\n'
        '4. Do not travel by road if water level is rising.\n'
        '5. Use rescue boats only if provided by authorities.\n'
        '6. Follow Kerala State Disaster Management Authority alerts.\n'
        '7. Do not attempt to swim through floodwater.',
        'en'),

        # ── EARTHQUAKE — English ──
        ('earthquake', 'Mumbai',
        '1. DROP to ground, take COVER under sturdy table, HOLD ON.\n'
        '2. Stay away from windows, mirrors, and heavy furniture.\n'
        '3. Do NOT run outside during shaking — injuries happen then.\n'
        '4. After shaking stops, exit building using stairs only.\n'
        '5. Move to open ground: Azad Maidan, Shivaji Park.\n'
        '6. Do not use elevators — they may be damaged.\n'
        '7. Stay away from damaged buildings and power lines.',
        'en'),

        ('earthquake', 'Pune',
        '1. DROP, COVER, and HOLD ON immediately.\n'
        '2. Move away from bookshelves, cabinets, and glass.\n'
        '3. After shaking stops, check for injuries before moving.\n'
        '4. Exit building carefully — check for cracks in stairs.\n'
        '5. Move to open areas: FC Road ground, Shivajinagar ground.\n'
        '6. Do not re-enter damaged buildings.\n'
        '7. Use SMS not calls — networks may be congested.',
        'en'),

        ('earthquake', 'Nashik',
        '1. Immediately DROP, COVER, and HOLD ON.\n'
        '2. Stay under a table or against an interior wall.\n'
        '3. Stay away from windows and exterior walls.\n'
        '4. After shaking stops, exit building cautiously.\n'
        '5. Assemble at open ground away from buildings.\n'
        '6. Check for gas leaks — if smell is present, open windows and leave.\n'
        '7. Do not light matches or use lighters after earthquake.',
        'en'),

        # ── FIRE — English ──
        ('fire', 'Mumbai',
        '1. Shout FIRE loudly and activate nearest fire alarm.\n'
        '2. Crawl low under smoke — clean air is near the floor.\n'
        '3. Feel every door before opening — if hot, use another exit.\n'
        '4. Use stairs ONLY — never elevators during a fire.\n'
        '5. Once outside, move to assembly point and do not re-enter.\n'
        '6. Call Mumbai Fire Brigade: 101.\n'
        '7. Wait for fire brigade at assembly point.',
        'en'),

        ('fire', 'Pune',
        '1. Alert everyone — shout and activate alarm.\n'
        '2. Crawl low under smoke to reach exit.\n'
        '3. Do not open hot doors — use alternate exit.\n'
        '4. Use staircase — never lift during fire.\n'
        '5. Meet at building assembly point outside.\n'
        '6. Call Pune Fire Brigade: 101.\n'
        '7. Never re-enter a burning building.',
        'en'),

        ('fire', 'Hyderabad',
        '1. Raise alarm immediately — shout FIRE.\n'
        '2. Activate manual call point or fire alarm.\n'
        '3. Escape using nearest staircase — crawl if smoky.\n'
        '4. Do not use lifts during fire emergency.\n'
        '5. Assemble at designated muster point outside.\n'
        '6. Call Hyderabad Fire Department: 101.\n'
        '7. Do not go back to collect belongings.',
        'en'),
        
            # ── LANDSLIDE — Wayanad (English) ──
        ('landslide', 'Wayanad',
        '1. Move away from hillsides and slopes immediately — do not wait.\n'
        '2. Avoid Mundakkai, Chooralmala, Meppadi, and Attamala areas.\n'
        '3. Listen for unusual sounds — cracking trees or rumbling means move NOW.\n'
        '4. Head to Kalpetta Government College Camp or Mananthavady Relief Centre.\n'
        '5. Do NOT try to cross rivers or streams — bridges may be damaged.\n'
        '6. Stay away from riverbanks — flash floods follow landslides.\n'
        '7. Follow Kerala Fire and Rescue and NDRF instructions only.',
        'en'),

        # ── FLOOD — Wayanad (English) ──
        ('flood', 'Wayanad',
        '1. Move to higher ground away from Chaliyar and Kabani river banks.\n'
        '2. Avoid tea and coffee plantation hillside areas during heavy rain.\n'
        '3. Do not attempt to cross any stream or river on foot.\n'
        '4. Head to Sulthan Bathery Camp or Kalpetta District Hospital Camp.\n'
        '5. Turn off electricity and gas before evacuating.\n'
        '6. Carry drinking water, torch, medicines, and ID documents.\n'
        '7. Follow Kerala SDMA (State Disaster Management Authority) alerts.',
        'en'),

        # ── LANDSLIDE — Wayanad (Malayalam) ──
        ('landslide', 'Wayanad',
        '1. കുന്നിൻ ചരിവുകളിൽ നിന്ന് ഉടൻ മാറുക — കാത്തിരിക്കരുത്.\n'
        '2. മുണ്ടക്കൈ, ചൂരൽമല, മേപ്പാടി, അട്ടമല പ്രദേശങ്ങൾ ഒഴിവാക്കുക.\n'
        '3. മരങ്ങൾ ഒടിയുന്ന ശബ്ദം കേട്ടാൽ ഉടൻ ഓടുക.\n'
        '4. കൽപ്പറ്റ ഗവൺമെൻ്റ് കോളേജ് ക്യാമ്പിലേക്ക് പോകുക.\n'
        '5. പുഴകളും തോടുകളും കടക്കാൻ ശ്രമിക്കരുത്.\n'
        '6. NDRF, Kerala Fire and Rescue നിർദ്ദേശങ്ങൾ പാലിക്കുക.',
        'ml'),

        # ── FLOOD — Wayanad (Malayalam) ──
        ('flood', 'Wayanad',
        '1. ചാലിയാർ, കബനി നദീതീരങ്ങളിൽ നിന്ന് മാറുക.\n'
        '2. തോട്ടപ്രദേശങ്ങളിൽ നിന്ന് ഉടൻ ഒഴിഞ്ഞുപോകുക.\n'
        '3. ഒരു തോടും കാൽനടയായി കടക്കരുത്.\n'
        '4. സുൽത്താൻ ബത്തേരി ക്യാമ്പിലേക്ക് പോകുക.\n'
        '5. വൈദ്യുതി ഓഫ് ചെയ്ത് മാത്രം പോകുക.\n'
        '6. Kerala SDMA അലർട്ടുകൾ ശ്രദ്ധിക്കുക.',
        'ml'),

        # ── FLOOD — Hindi ──
        ('flood', 'Mumbai',
        '1. तुरंत ऊंचे स्थान पर जाएं।\n'
        '2. माहिम, कुर्ला, धारावी के निचले इलाकों से दूर रहें।\n'
        '3. बहते पानी में न चलें।\n'
        '4. आज़ाद मैदान राहत शिविर में जाएं।\n'
        '5. जाने से पहले बिजली का मुख्य स्विच बंद करें।',
        'hi'),

        ('flood', 'Pune',
        '1. मुला-मुथा नदी के किनारों से तुरंत दूर जाएं।\n'
        '2. शिवाजीनगर राहत केंद्र में जाएं।\n'
        '3. जलभराव वाली सड़कों पर गाड़ी न चलाएं।\n'
        '4. बिजली बंद करके निकलें।\n'
        '5. अधिकारियों के निर्देशों का पालन करें।',
        'hi'),

        # ── FLOOD — Malayalam ──
        ('flood', 'Kochi',
        '1. ഉടൻ ഉയർന്ന സ്ഥലത്തേക്ക് മാറുക.\n'
        '2. കായലോരങ്ങളിൽ നിന്ന് അകലുക.\n'
        '3. എർണാകുളം റിലീഫ് സെന്ററിലേക്ക് പോകുക.\n'
        '4. വെള്ളക്കെട്ടുള്ള റോഡിലൂടെ സഞ്ചരിക്കരുത്.\n'
        '5. KSDC യുടെ നിർദ്ദേശങ്ങൾ പാലിക്കുക.',
        'ml'),

        # ── FLOOD — Tamil ──
        ('flood', 'Chennai',
        '1. உடனே உயரமான இடத்திற்கு செல்லுங்கள்.\n'
        '2. அடைபட்ட சாலைகளில் வாகனம் ஓட்டாதீர்கள்.\n'
        '3. மரீனா கடற்கரை நிவாரண முகாமுக்கு செல்லுங்கள்.\n'
        '4. மின்சாரம் அணைத்துவிட்டு வெளியேறுங்கள்.\n'
        '5. அதிகாரிகளின் அறிவிப்புகளை கேளுங்கள்.',
        'ta'),

        # ── FLOOD — Telugu ──
        ('flood', 'Hyderabad',
        '1. వెంటనే ఎత్తైన ప్రదేశానికి వెళ్ళండి.\n'
        '2. మూసీ నది పరిసరాల నుండి దూరంగా ఉండండి.\n'
        '3. LB స్టేడియం రిలీఫ్ క్యాంప్‌కు వెళ్ళండి.\n'
        '4. విద్యుత్ స్విచ్ ఆపివేసి వెళ్ళండి.\n'
        '5. NDRF సూచనలను పాటించండి.',
        'te'),

        # ── FLOOD — Kannada ──
        ('flood', 'Bangalore',
        '1. ತಕ್ಷಣ ಎತ್ತರದ ಪ್ರದೇಶಕ್ಕೆ ಹೋಗಿ.\n'
        '2. ರಾಜಕಾಲುವೆ ಪ್ರದೇಶಗಳಿಂದ ದೂರ ಇರಿ.\n'
        '3. ಕಬ್ಬನ್ ಪಾರ್ಕ್ ರಿಲೀಫ್ ಕ್ಯಾಂಪ್‌ಗೆ ಹೋಗಿ.\n'
        '4. ನೀರು ತುಂಬಿದ ರಸ್ತೆಗಳಲ್ಲಿ ವಾಹನ ಓಡಿಸಬೇಡಿ.\n'
        '5. BBMP ಸೂಚನೆಗಳನ್ನು ಅನುಸರಿಸಿ.',
        'kn'),

        # ── FLOOD — Marathi ──
        ('flood', 'Nashik',
        '1. गोदावरी नदीच्या काठापासून ताबडतोब दूर व्हा.\n'
        '2. पंचवटी भागातून बाहेर पडा.\n'
        '3. नाशिक जिल्हा राहत शिविरात जा.\n'
        '4. पूरग्रस्त रस्त्यावर वाहन चालवू नका.\n'
        '5. महानगरपालिकेच्या सूचना ऐका.',
        'mr'),
    ]

    # Insert all data (ignore if already exists)
    # CORRECT — all languages included
    # CORRECT — all languages included
    
    print(f"    EN: {len(first_aid_en)}")
    print(f"    HI: {len(first_aid_hi)}")
    print(f"    ML: {len(first_aid_ml)}")
    print(f"    TA: {len(first_aid_ta)}")
    print(f"    TE: {len(first_aid_te)}")
    print(f"    KN: {len(first_aid_kn)}")
    
    # CORRECT
    all_first_aid = (
        first_aid_en +
        first_aid_hi +
        first_aid_ml +
        first_aid_ta +
        first_aid_te +
        first_aid_kn
    )
    print(f"    Total to insert: {len(all_first_aid)}")
    cursor.executemany(
        'INSERT OR REPLACE INTO first_aid (condition, steps, language) VALUES (?, ?, ?)',
        all_first_aid
    )
    
    cursor.executemany(
        'INSERT OR REPLACE INTO shelters (name, address, city, capacity, lat, lng) VALUES (?, ?, ?, ?, ?, ?)',
        shelters
    )
    
    cursor.executemany(
        'INSERT OR REPLACE INTO evacuation_routes (disaster_type, region, instructions, language) VALUES (?, ?, ?, ?)',
        evacuation
    )
    
    # ─────────────────────────────────────────────────────
    # DISASTER PRONE AREAS DATA
    # ─────────────────────────────────────────────────────
    disaster_prone_areas = [

        # ════════════════════════════════
        # KERALA
        # ════════════════════════════════
        ('Mundakkai-Chooralmala',  'Wayanad',     'Kerala',       'landslide',  'HIGH',
        'Steep Western Ghats slopes with fragile soil, deforestation, and heavy monsoon rainfall',
        'Kalpetta town, Mananthavady town centre, Sultan Bathery flat areas', 'en'),

        ('Meppadi',                'Wayanad',     'Kerala',       'landslide',  'HIGH',
        'Located on steep terrain with tea plantation soil erosion and high rainfall zone',
        'Vythiri Junction, Kalpetta Government College Camp', 'en'),

        ('Munnar',                 'Idukki',      'Kerala',       'landslide',  'HIGH',
        'High altitude hilly terrain with heavy rainfall and unstable slopes',
        'Munnar town centre, Devikulam flat area', 'en'),

        ('Idukki',                 'Idukki',      'Kerala',       'flood',      'HIGH',
        'Located near Periyar River basin, dam-dependent region vulnerable to controlled releases',
        'Thodupuzha town, Ernakulam district', 'en'),

        ('Kuttanad',               'Alappuzha',   'Kerala',       'flood',      'HIGH',
        'Below sea level agricultural region — floods every monsoon season',
        'Alappuzha town, Changanacherry', 'en'),

        ('Chalakudy',              'Thrissur',    'Kerala',       'flood',      'HIGH',
        'Situated along Chalakudy River which floods every heavy monsoon season',
        'Thrissur town, Irinjalakuda', 'en'),

        ('Kozhikode Coast',        'Kozhikode',   'Kerala',       'cyclone',    'MEDIUM',
        'Arabian Sea coastal area exposed to low pressure systems and cyclonic storms',
        'Inland Kozhikode city areas, higher ground settlements', 'en'),

        ('Ernakulam Lowlands',     'Ernakulam',   'Kerala',       'flood',      'HIGH',
        'Urban flooding due to blocked drainage, Periyar River overflow, and coastal backwaters',
        'MG Road elevated areas, Kakkanad IT corridor', 'en'),

        # ════════════════════════════════
        # MAHARASHTRA
        # ════════════════════════════════
        ('Raigad Coast',           'Raigad',      'Maharashtra',  'cyclone',    'HIGH',
        'Konkan coastline directly exposed to Arabian Sea cyclones',
        'Inland Pen, Panvel areas away from coast', 'en'),

        ('Kolhapur City',          'Kolhapur',    'Maharashtra',  'flood',      'HIGH',
        'Located on Panchaganga River banks which overflow severely every monsoon',
        'Tarabai Park elevated area, Rajaram College Ground', 'en'),

        ('Sangli',                 'Sangli',      'Maharashtra',  'flood',      'HIGH',
        'Krishna River floods regularly affecting low-lying areas of Sangli and Miraj',
        'Higher residential areas away from riverbank', 'en'),

        ('Nashik River Belt',      'Nashik',      'Maharashtra',  'flood',      'HIGH',
        'Godavari River and its tributaries flood Panchavati and old Nashik areas',
        'Nashik Road area, Gangapur Dam surroundings on high ground', 'en'),

        ('Mumbai Coastal Areas',   'Mumbai',      'Maharashtra',  'cyclone',    'HIGH',
        'Marine Drive, Bandra, Versova coast exposed to Arabian Sea cyclones and storm surge',
        'Eastern suburbs, inland Thane, Navi Mumbai elevated areas', 'en'),

        ('Dharavi-Kurla Belt',     'Mumbai',      'Maharashtra',  'flood',      'HIGH',
        'Low-lying urban slums near Mithi River with severe monsoon flooding history',
        'BKC elevated area, Powai, Vikhroli hills', 'en'),

        ('Konkan Region',          'Ratnagiri',   'Maharashtra',  'landslide',  'HIGH',
        'Heavy Western Ghats rainfall causes road and hillside landslides every monsoon',
        'Ratnagiri town centre, Chiplun market area', 'en'),

        ('Osmanabad',              'Osmanabad',   'Maharashtra',  'drought',    'HIGH',
        'Marathwada region with historically low rainfall and recurring drought conditions',
        'Government water supply zones, Osmanabad city', 'en'),

        ('Latur',                  'Latur',       'Maharashtra',  'earthquake', 'HIGH',
        'Seismically active zone — 1993 earthquake killed over 10,000 people here',
        'Open grounds, away from old masonry buildings', 'en'),

        # ════════════════════════════════
        # ANDHRA PRADESH & TELANGANA
        # ════════════════════════════════
        ('Vijayawada',             'Krishna',     'Andhra Pradesh', 'flood',    'HIGH',
        'Located on Krishna River banks — floods frequently during monsoon season',
        'Elevated Amaravati area, Guntur district', 'en'),

        ('Srikakulam Coast',       'Srikakulam',  'Andhra Pradesh', 'cyclone',  'HIGH',
        'Northern Andhra coast most frequently hit by Bay of Bengal cyclones',
        'Inland Srikakulam town, Palasa', 'en'),

        ('Godavari Delta',         'East Godavari','Andhra Pradesh','flood',    'HIGH',
        'Godavari River delta floods regularly — one of the most flood-prone zones in India',
        'Rajahmundry elevated areas, Kakinada higher zones', 'en'),

        ('Hyderabad Musi Belt',    'Hyderabad',   'Telangana',    'flood',      'HIGH',
        'Musi River overflows affect Moosarambagh, Amberpet, and old city low areas',
        'LB Nagar elevated areas, Secunderabad', 'en'),

        ('Bhadrachalam',           'Bhadradri',   'Telangana',    'flood',      'HIGH',
        'Located on Godavari River which floods heavily during monsoon every year',
        'Higher areas of Bhadrachalam town', 'en'),

        # ════════════════════════════════
        # KARNATAKA
        # ════════════════════════════════
        ('Kodagu (Coorg)',         'Kodagu',      'Karnataka',    'landslide',  'HIGH',
        'Heavy Western Ghats rainfall on steep coffee plantation slopes',
        'Madikeri town centre, Kushalnagar', 'en'),

        ('Uttara Kannada Coast',   'Uttara Kannada','Karnataka',  'cyclone',    'MEDIUM',
        'Karwar and Gokarna coastline exposed to Arabian Sea weather systems',
        'Sirsi inland area, Dharwad', 'en'),

        ('Belagavi',               'Belagavi',    'Karnataka',    'flood',      'HIGH',
        'Krishna River tributaries flood low-lying areas of Belagavi every monsoon',
        'Elevated residential areas of Belagavi city', 'en'),

        ('Raichur',                'Raichur',     'Karnataka',    'flood',      'HIGH',
        'Krishna and Tungabhadra River confluence creates severe floods',
        'Higher ground areas of Raichur city', 'en'),

        # ════════════════════════════════
        # TAMIL NADU
        # ════════════════════════════════
        ('Chennai Coast',          'Chennai',     'Tamil Nadu',   'cyclone',    'HIGH',
        'Bay of Bengal coastline — Chennai receives multiple cyclones every decade',
        'Inland Anna Nagar, Tambaram, Chromepet', 'en'),

        ('Cuddalore',              'Cuddalore',   'Tamil Nadu',   'cyclone',    'HIGH',
        'One of the most cyclone-hit districts in Tamil Nadu on Bay of Bengal coast',
        'Inland Virudhachalam, Neyveli', 'en'),

        ('Nagapattinam',           'Nagapattinam','Tamil Nadu',   'cyclone',    'HIGH',
        '2004 Tsunami and multiple cyclones have devastated this coastal district',
        'Inland Mayiladuthurai, Kumbakonam', 'en'),

        ('Nilgiris',               'Nilgiris',    'Tamil Nadu',   'landslide',  'HIGH',
        'Tea estate slopes with fragile soil and extremely heavy Northeast monsoon rainfall',
        'Ooty town centre, Coonoor flat areas', 'en'),

        ('Dharmapuri',             'Dharmapuri',  'Tamil Nadu',   'drought',    'HIGH',
        'Inland Tamil Nadu with low rainfall and recurring drought conditions',
        'Government water supply zones in Dharmapuri city', 'en'),

        # ════════════════════════════════
        # ODISHA
        # ════════════════════════════════
        ('Puri Coast',             'Puri',        'Odisha',       'cyclone',    'HIGH',
        'Most cyclone-prone state in India — Puri coast directly faces Bay of Bengal',
        'Inland Bhubaneswar, elevated areas 50 km from coast', 'en'),

        ('Kendrapara',             'Kendrapara',  'Odisha',       'cyclone',    'HIGH',
        'Bhitarkanika coast — hit by Super Cyclone 1999 and multiple storms since',
        'Inland Cuttack, Bhubaneswar', 'en'),

        ('Mahanadi Delta',         'Cuttack',     'Odisha',       'flood',      'HIGH',
        'Mahanadi River delta floods entire downstream coastal districts every monsoon',
        'Elevated Cuttack city areas, Bhubaneswar', 'en'),

        # ════════════════════════════════
        # UTTARAKHAND
        # ════════════════════════════════
        ('Kedarnath Valley',       'Rudraprayag', 'Uttarakhand',  'landslide',  'HIGH',
        '2013 flash flood killed thousands — extreme rainfall on fragile Himalayan slopes',
        'Guptkashi, Agastmuni on relatively stable ground', 'en'),

        ('Chamoli',                'Chamoli',     'Uttarakhand',  'flood',      'HIGH',
        'Alaknanda River and glacial lake outburst floods threaten this district regularly',
        'Gopeshwar town on higher stable ground', 'en'),

        ('Pithoragarh',            'Pithoragarh', 'Uttarakhand',  'landslide',  'HIGH',
        'High Himalayan terrain with severe landslides blocking roads during monsoon',
        'Pithoragarh town centre on plateau', 'en'),

        # ════════════════════════════════
        # GUJARAT
        # ════════════════════════════════
        ('Kutch',                  'Kutch',       'Gujarat',      'earthquake', 'HIGH',
        '2001 earthquake killed 20,000 people — remains one of India most seismic zones',
        'RCC constructed buildings, open grounds away from old structures', 'en'),

        ('Saurashtra Coast',       'Jamnagar',    'Gujarat',      'cyclone',    'HIGH',
        'Arabian Sea cyclones frequently strike Saurashtra and Kutch coastline',
        'Inland Rajkot, Surendranagar', 'en'),

        ('Ahmedabad Low Areas',    'Ahmedabad',   'Gujarat',      'flood',      'MEDIUM',
        'Sabarmati River floods low-lying slum areas of Ahmedabad during heavy rainfall',
        'Elevated satellite areas, GIFT City', 'en'),

        # ════════════════════════════════
        # ASSAM AND NORTHEAST
        # ════════════════════════════════
        ('Brahmaputra Valley',     'Kamrup',      'Assam',        'flood',      'HIGH',
        'Brahmaputra floods every year destroying villages across 28 districts of Assam',
        'Dispur elevated areas, Guwahati hills', 'en'),

        ('Kaziranga',              'Golaghat',    'Assam',        'flood',      'HIGH',
        'Annual Brahmaputra floods submerge Kaziranga and surrounding villages',
        'Higher ground of Bokakhat, Golaghat town', 'en'),

        ('Manipur Hills',          'Senapati',    'Manipur',      'landslide',  'HIGH',
        'Heavy rainfall on unstable hill terrain causes frequent road and village landslides',
        'Imphal valley flat areas, Imphal city', 'en'),

        # ════════════════════════════════
        # HIMACHAL PRADESH
        # ════════════════════════════════
        ('Kullu Valley',           'Kullu',       'Himachal Pradesh', 'landslide', 'HIGH',
        'Beas River valley with steep slopes — 2023 floods caused massive destruction',
        'Bhuntar flat area, Manali town centre', 'en'),

        ('Shimla Outskirts',       'Shimla',      'Himachal Pradesh', 'landslide', 'MEDIUM',
        'Old construction on steep slopes vulnerable to rain-triggered landslides',
        'Shimla Ridge area, Sanjauli on stable ground', 'en'),

        # ════════════════════════════════
        # HINDI TRANSLATIONS — KEY AREAS
        # ════════════════════════════════
        ('मुंडक्कई-चूरलमला',      'वायनाड',     'केरल',          'landslide',  'HIGH',
        'पश्चिमी घाट की खड़ी ढलानें, मिट्टी का क्षरण और भारी वर्षा',
        'कल्पेट्टा शहर, मनंतवाडी राहत केंद्र', 'hi'),

        ('कुट्टनाड',               'अलाप्पुझा',  'केरल',          'flood',      'HIGH',
        'समुद्र तल से नीचे कृषि क्षेत्र — हर मानसून में बाढ़ आती है',
        'अलाप्पुझा शहर, चंगनाचेरी', 'hi'),

        ('कोल्हापुर',              'कोल्हापुर',  'महाराष्ट्र',    'flood',      'HIGH',
        'पंचगंगा नदी हर मानसून में भारी बाढ़ लाती है',
        'ताराबाई पार्क उच्च क्षेत्र, राजाराम कॉलेज ग्राउंड', 'hi'),

        ('भुज-कच्छ',              'कच्छ',       'गुजरात',         'earthquake', 'HIGH',
        '2001 में 20,000 लोगों की मौत — भारत का सबसे भूकंप प्रवण क्षेत्र',
        'खुले मैदान, RCC इमारतें', 'hi'),

        # ════════════════════════════════
        # MALAYALAM TRANSLATIONS
        # ════════════════════════════════
        ('മുണ്ടക്കൈ-ചൂരൽമല',      'വയനാട്',     'കേരളം',         'landslide',  'HIGH',
        'പശ്ചിമഘട്ടത്തിലെ ചരിഞ്ഞ ഭൂമി, വനനശീകരണം, കനത്ത മഴ',
        'കൽപ്പറ്റ പട്ടണം, മാനന്തവാടി', 'ml'),

        ('കുട്ടനാട്',             'ആലപ്പുഴ',    'കേരളം',         'flood',      'HIGH',
        'സമുദ്രനിരപ്പിന് താഴെ — ഓരോ മൺസൂണിലും വെള്ളപ്പൊക്കം',
        'ആലപ്പുഴ പട്ടണം, ചങ്ങനാശ്ശേരി', 'ml'),

        ('ഇടുക്കി',               'ഇടുക്കി',    'കേരളം',         'flood',      'HIGH',
        'ഡാം നിയന്ത്രിത പ്രദേശം — ഷട്ടർ തുറക്കുമ്പോൾ വെള്ളപ്പൊക്കം',
        'തൊടുപുഴ പട്ടണം, എറണാകുളം', 'ml'),

        ('കോഴിക്കോട് തീരം',      'കോഴിക്കോട്', 'കേരളം',         'cyclone',    'MEDIUM',
        'അറബിക്കടൽ തീരം — ന്യൂനമർദ്ദവും കൊടുങ്കാറ്റും',
        'കോഴിക്കോട് ഉൾഭൂമി, കൂടല്ലൂർ', 'ml'),

        # ════════════════════════════════
        # TAMIL TRANSLATIONS
        # ════════════════════════════════
        ('சென்னை கடற்கரை',        'சென்னை',     'தமிழ்நாடு',    'cyclone',    'HIGH',
        'வங்காள விரிகுடா கடற்கரை — அடிக்கடி சூறாவளி வரும் பகுதி',
        'உள்நாட்டு அண்ணா நகர், தாம்பரம்', 'ta'),

        ('நீலகிரி',               'நீலகிரி',    'தமிழ்நாடு',    'landslide',  'HIGH',
        'தேயிலை தோட்ட சரிவுகள் மற்றும் கனமழை — மண்சரிவு அதிகம்',
        'ஊட்டி நகர் மையம், கூனூர் சமவெளி பகுதி', 'ta'),

        # ════════════════════════════════
        # TELUGU TRANSLATIONS
        # ════════════════════════════════
        ('హైదరాబాద్ మూసీ బెల్ట్', 'హైదరాబాద్', 'తెలంగాణ',      'flood',      'HIGH',
        'మూసీ నది ఉప్పొంగి తక్కువ ప్రాంతాలు ముంపుకు గురవుతాయి',
        'LB నగర్ ఎత్తైన ప్రాంతాలు, సికింద్రాబాద్', 'te'),

        ('గోదావరి డెల్టా',        'తూర్పు గోదావరి', 'ఆంధ్రప్రదేశ్', 'flood',  'HIGH',
        'గోదావరి నది డెల్టా ప్రతి మానసూన్‌లో వరదలకు గురవుతుంది',
        'రాజమహేంద్రవరం ఎత్తైన ప్రాంతాలు', 'te'),

        # ════════════════════════════════
        # KANNADA TRANSLATIONS
        # ════════════════════════════════
        ('ಕೊಡಗು',                 'ಕೊಡಗು',      'ಕರ್ನಾಟಕ',      'landslide',  'HIGH',
        'ಕಾಫಿ ತೋಟದ ಇಳಿಜಾರು ಮತ್ತು ಭಾರೀ ಮಳೆ — ಭೂಕುಸಿತ ಸಾಮಾನ್ಯ',
        'ಮಡಿಕೇರಿ ಪಟ್ಟಣ, ಕುಶಾಲನಗರ', 'kn'),

        ('ಬೆಳಗಾವಿ',               'ಬೆಳಗಾವಿ',    'ಕರ್ನಾಟಕ',      'flood',      'HIGH',
        'ಕೃಷ್ಣಾ ನದಿ ಉಪನದಿಗಳು ಪ್ರತಿ ಮಳೆಗಾಲದಲ್ಲಿ ಪ್ರವಾಹ ತರುತ್ತವೆ',
        'ಬೆಳಗಾವಿ ನಗರದ ಎತ್ತರದ ಪ್ರದೇಶಗಳು', 'kn'),

        # ════════════════════════════════
        # MARATHI TRANSLATIONS
        # ════════════════════════════════
        ('कोल्हापूर शहर',         'कोल्हापूर',  'महाराष्ट्र',   'flood',      'HIGH',
        'पंचगंगा नदी दरवर्षी मोठी पूर आणते — शहराचा मोठा भाग बुडतो',
        'ताराबाई पार्क उंच भाग, राजाराम कॉलेज ग्राउंड', 'mr'),

        ('कोकण किनारपट्टी',       'रत्नागिरी',  'महाराष्ट्र',   'landslide',  'HIGH',
        'पश्चिम घाटावर अतिवृष्टीमुळे दरड कोसळणे नित्याचे',
        'रत्नागिरी शहर केंद्र, चिपळूण बाजार', 'mr'),
    ]

    cursor.executemany(
            'INSERT OR REPLACE INTO disaster_prone_areas '
            '(area_name, district, state, disaster_type, risk_level, reason, safe_zones, language) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            disaster_prone_areas
    )

    conn.commit()
    conn.close()

        # ── Verify final counts from DB ──
    verify_conn = get_connection()
    fa_count    = verify_conn.execute('SELECT COUNT(*) FROM first_aid').fetchone()[0]
    sh_count    = verify_conn.execute('SELECT COUNT(*) FROM shelters').fetchone()[0]
    ev_count    = verify_conn.execute('SELECT COUNT(*) FROM evacuation_routes').fetchone()[0]
    dp_count    = verify_conn.execute('SELECT COUNT(*) FROM disaster_prone_areas').fetchone()[0]
    verify_conn.close()

    print(f"Database seeded successfully at: emergency.db")
    print(f"  First aid entries: {fa_count}")
    print(f"  Shelters:          {sh_count}")
    print(f"  Evacuation routes: {ev_count}")
    print(f"  Disaster prone areas: {dp_count}")

if __name__ == '__main__':
    seed()
    print("Database seeded successfully!")