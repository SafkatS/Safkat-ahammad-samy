"""GoodBuy Foods Global — Bangladesh export product directory.

Edit this list, then run:  python3 tools/build_site.py
HS = 4-digit heading (indicative). Confirm the full 8-digit code with your customs broker per shipment.
Markets = typical buyer markets for Bangladeshi supply (indicative).
"""

CATEGORIES = [
  # id, title, group, intro (answer-first, used on page and in structured data)
  ("shrimp", "Shrimp & prawn", "fish", "Bangladesh's largest seafood export. Farmed in the south-west (Khulna, Satkhira, Bagerhat) and processed in EU-approved plants."),
  ("shell", "Crab, lobster & molluscs", "fish", "Live mud crab goes mainly to East Asia by air. Squid and cuttlefish come from Bay of Bengal trawlers and are frozen at Chattogram."),
  ("marine", "Marine finfish", "fish", "Wild-caught in the Bay of Bengal and landed at Chattogram, Cox's Bazar and Mongla. Most is frozen whole for the Middle East and East Asia."),
  ("fresh", "Freshwater & farmed fish", "fish", "Carp, catfish and other river and pond fish, exported chilled or frozen to South Asian communities in the UK, the Middle East and North America."),
  ("live", "Live eel & specialty", "fish", "Live mud eel (kuchia) is flown to China and South Korea. It needs plants approved by the importing country, such as GACC registration for China."),
  ("dried", "Dried, salted & by-products", "fish", "Sun-dried sea fish (shutki) from Cox's Bazar and Chattogram, salted hilsa, fish maw and fish scales."),
  ("rice", "Rice & grains", "food", "Small-grain aromatic rice and traditional rice products. Aromatic rice exports depend on current government export policy."),
  ("spice", "Spices, tea & leaf", "food", "Turmeric, chilli, coriander and black cumin, plus Sylhet tea and betel leaf."),
  ("veg", "Fresh vegetables", "food", "Air- and sea-freighted vegetables for South Asian diaspora markets and nearby Asian buyers."),
  ("fruit", "Fresh fruits", "food", "Seasonal mango, jackfruit, pineapple and lychee. Mango is shipped under the Department of Agricultural Extension's quarantine protocol."),
  ("frozen", "Frozen & ready-to-cook", "food", "IQF vegetables, frozen paratha and frozen snacks from Bangladeshi food processors."),
  ("sweet", "Sugar, jaggery & sweeteners", "food", "Traditional date-palm and cane jaggery, molasses and honey from Jashore, the Sundarbans and the mustard belt."),
  ("processed", "Processed & packaged foods", "food", "Biscuits, noodles, snacks, juices, fruit pulp, pickles, sauces, spice mixes, ready mixes and edible oils from Bangladeshi food processors, many with international distribution."),
]

# id, cat, name, local (Bangla name), scientific, HS heading, forms, markets, note, featured
P = [
 # ---- Shrimp & prawn
 ("bt","shrimp","Black tiger shrimp","Bagda chingri","Penaeus monodon","0306","HOSO, HLSO, PD, PDTO, PUD, Nobashi, cooked","EU · UK · USA · Japan","",True),
 ("gp","shrimp","Giant freshwater prawn","Golda chingri","Macrobrachium rosenbergii","0306","HOSO, HLSO, PUD","EU · UK · Middle East","",True),
 ("vn","shrimp","Whiteleg shrimp","Vannamei","Litopenaeus vannamei","0306","HLSO, PD, PDTO, cooked","EU · USA","Commercial farming in Bangladesh began recently, so volumes are still growing.",False),
 ("iw","shrimp","Indian white shrimp","Chaka chingri","Fenneropenaeus indicus","0306","HOSO, HLSO, PUD","EU · Japan","",False),
 ("br","shrimp","Speckled (brown) shrimp","Harina chingri","Metapenaeus monoceros","0306","HOSO, PUD, PD","EU · Middle East","",False),
 ("sf","shrimp","Small freshwater shrimp","Gura chingri","Macrobrachium spp.","0306","Frozen block","UK · Middle East","",False),
 ("va","shrimp","Value-added shrimp","","Penaeus spp.","1605","Breaded, cooked ring, skewered","EU · USA","",False),
 # ---- Crab, lobster & molluscs
 ("mc","shell","Mud crab","Shila kakra","Scylla serrata / S. olivacea","0306","Live (air freight), frozen","China · Taiwan · Malaysia · Singapore","Live crab for China must come from a GACC-registered exporter.",True),
 ("sc","shell","Soft-shell crab","Narom kakra","Scylla spp.","0306","Frozen whole, cleaned","USA · Japan · EU","",False),
 ("lb","shell","Spiny lobster","Lobster","Panulirus spp.","0306","Frozen whole, tails","China · Middle East","Small seasonal volumes.",False),
 ("sq","shell","Squid","Squid","Uroteuthis duvaucelii","0307","Whole cleaned, tubes, rings","EU · China · Japan","",False),
 ("cu","shell","Cuttlefish","Cuttlefish","Sepia pharaonis","0307","Whole cleaned, fillet","EU · Japan · China","",False),
 ("oc","shell","Octopus","Octopus","Octopus spp.","0307","Whole frozen","EU","Limited volumes.",False),
 # ---- Marine finfish
 ("hl","marine","Hilsa","Ilish","Tenualosa ilisha","0302 / 0303","Whole fresh, whole frozen","India · Middle East · UK · USA","Exports need a government permit and are limited to published quotas and seasons.",True),
 ("ks","marine","Kelee shad","Chandana ilish","Hilsa kelee","0303","Whole frozen","Middle East","",False),
 ("sp","marine","Silver pomfret","Rupchanda","Pampus argenteus","0303","Whole round IQF","Middle East · China · EU","",True),
 ("cp","marine","Chinese pomfret","Chinese rupchanda","Pampus chinensis","0303","Whole round IQF","Middle East · China","",False),
 ("bp","marine","Black pomfret","Halua chanda","Parastromateus niger","0303","Whole round frozen","Middle East · China","",False),
 ("rb","marine","Ribbonfish","Churi","Trichiurus lepturus","0303","Whole, block frozen","China · Middle East · South Korea","",False),
 ("bd","marine","Bombay duck","Loitta","Harpadon nehereus","0303","Whole frozen","UK · Middle East","",False),
 ("pc","marine","Pama croaker","Poa","Otolithoides pama","0303","Whole frozen","Middle East · China","",False),
 ("it","marine","Indian threadfin","Lakkha","Leptomelanosoma indicum","0303","Whole frozen, steaks","Middle East · China","",False),
 ("ft","marine","Fourfinger threadfin","Tailla","Eleutheronema tetradactylum","0303","Whole frozen","Middle East","",False),
 ("km","marine","Indo-Pacific king mackerel","Maitta","Scomberomorus guttatus","0303","Whole, steaks","Middle East","",False),
 ("im","marine","Indian mackerel","","Rastrelliger kanagurta","0303","Whole frozen","Middle East · Sri Lanka","",False),
 ("rs","marine","Red snapper","","Lutjanus spp.","0302 / 0303","Whole on ice, gutted, fillet","Middle East · EU","",True),
 ("gr","marine","Grouper","","Epinephelus spp.","0302 / 0303","Whole on ice, frozen","Middle East · East Asia","",False),
 ("bm","marine","Barramundi (Asian sea bass)","Bhetki / Koral","Lates calcarifer","0302 / 0303 / 0304","Whole, fillet","EU · UK · Middle East","",False),
 ("ml","marine","Mullet","Parse","Planiliza parsia / Mugil cephalus","0302 / 0303","Whole chilled or frozen","UK · Middle East","",False),
 ("sb","marine","Yellowfin seabream","Datina","Acanthopagrus latus","0303","Whole frozen","Middle East","",False),
 ("gt","marine","Grunt","","Pomadasys spp.","0303","Whole frozen","Middle East","",False),
 ("tn","marine","Tuna (skipjack, yellowfin)","","Katsuwonus pelamis / Thunnus albacares","0303","Whole frozen","Middle East","Mostly from deep-sea trawlers.",False),
 ("bc","marine","Barracuda","","Sphyraena spp.","0303","Whole frozen","Middle East","",False),
 ("tt","marine","Tripletail","","Lobotes surinamensis","0302","Whole chilled","Middle East","",False),
 # ---- Freshwater & farmed
 ("pg","fresh","Pangasius","Pangas","Pangasianodon hypophthalmus","0302 / 0303 / 0304","Whole, fillet","Middle East · South Asian diaspora","",True),
 ("tl","fresh","Tilapia","Telapia","Oreochromis niloticus","0302 / 0303 / 0304","Whole gutted, fillet","Middle East · EU · USA","",False),
 ("rh","fresh","Rohu","Rui","Labeo rohita","0302 / 0303","Whole, steaks, curry cut","UK · Middle East · USA · India","",True),
 ("ct","fresh","Catla","Katla","Catla catla","0302 / 0303","Whole, steaks","UK · Middle East · USA","",False),
 ("mg","fresh","Mrigal","Mrigel","Cirrhinus mrigala","0302 / 0303","Whole, steaks","UK · Middle East","",False),
 ("kb","fresh","Kalbasu","Kalibaus","Labeo calbasu","0302 / 0303","Whole","UK · Middle East","",False),
 ("sv","fresh","Silver carp","Silver carp","Hypophthalmichthys molitrix","0302 / 0303","Whole, steaks","Middle East · India","",False),
 ("ko","fresh","Climbing perch","Koi","Anabas testudineus","0301 / 0302","Live, chilled","UK · Middle East","",False),
 ("sh","fresh","Stinging catfish","Shing","Heteropneustes fossilis","0301 / 0302","Live, chilled","UK · Middle East","",False),
 ("mr","fresh","Walking catfish","Magur","Clarias batrachus","0301 / 0302","Live, chilled","UK · Middle East","",False),
 ("so","fresh","Striped snakehead","Shol","Channa striata","0302 / 0303","Whole chilled or frozen","UK · Middle East","",False),
 ("gj","fresh","Giant snakehead","Gojar","Channa marulius","0302 / 0303","Whole chilled or frozen","UK · Middle East","",False),
 ("wa","fresh","Wallago catfish","Boal","Wallago attu","0302 / 0303","Whole, steaks","UK · Middle East","",False),
 ("ai","fresh","Long-whiskered catfish","Aair","Sperata aor","0302 / 0303","Whole, steaks","UK · Middle East","",False),
 ("pb","fresh","Pabda catfish","Pabda","Ompok pabda","0302 / 0303","Whole chilled or frozen","UK · Middle East · USA","",False),
 ("gu","fresh","Gulsha tengra","Gulsha","Mystus cavasius","0302 / 0303","Whole chilled or frozen","Middle East · UK","",False),
 ("tg","fresh","Tengra catfish","Tengra","Mystus tengara","0302 / 0303","Whole frozen","UK · Middle East","",False),
 ("cl","fresh","Clown knifefish","Chital","Chitala chitala","0302 / 0303","Whole, steaks","UK · Middle East","",False),
 ("mo","fresh","Mola carplet","Mola","Amblypharyngodon mola","0303","Frozen block","UK · Middle East","",False),
 ("pu","fresh","Puti barb","Puti","Puntius spp.","0303","Frozen block","UK · Middle East","",False),
 # ---- Live & specialty
 ("ee","live","Mud eel","Kuchia","Monopterus cuchia","0301","Live (air freight)","China · South Korea · Taiwan","The importing country must approve the exporter (for China, GACC registration).",True),
 # ---- Dried, salted & by-products
 ("dl","dried","Dried Bombay duck","Loitta shutki","Harpadon nehereus","0305","Sun-dried, salt-free","UK · Middle East · USA","",False),
 ("dr","dried","Dried ribbonfish","Churi shutki","Trichiurus lepturus","0305","Sun-dried","UK · Middle East","",False),
 ("ds","dried","Dried shrimp","Chingri shutki","Acetes / Metapenaeus spp.","0306","Sun-dried","UK · Middle East","",False),
 ("dm","dried","Mixed dried sea fish","Shutki","Assorted marine species","0305","Sun-dried, vacuum packed","UK · Middle East · USA","",False),
 ("nh","dried","Salted hilsa","Nona ilish","Tenualosa ilisha","0305","Salted, cured","Middle East · UK","Subject to the same permit rules as hilsa.",False),
 ("fm","dried","Fish maw (swim bladder)","Fish maw","Croaker / catfish species","0305","Dried","China · Hong Kong","",False),
 ("fs","dried","Fish scales","Fish scales","Assorted species","0511","Cleaned, dried","China · Japan","Used for collagen extraction.",False),
 ("fo","dried","Fish oil","Fish oil","Assorted species","1504","Crude","Asia","",False),
 # ---- Rice & grains
 ("ar","rice","Aromatic rice (Kalijira, Chinigura, Kataribhog)","Sugandhi chal","Oryza sativa","1006","Milled, parboiled; 1–25 kg","Middle East · UK · USA · EU","Exports depend on current government export policy.",True),
 ("mu","rice","Puffed rice","Muri","Oryza sativa","1904","Retail packs","UK · Middle East · USA","",False),
 ("ch","rice","Flattened rice","Chira","Oryza sativa","1904","Retail packs","UK · Middle East · USA","",False),
 ("se","rice","Vermicelli & laccha semai","Semai","Wheat","1902","Retail packs","Middle East · UK","",False),
 # ---- Spices, tea & leaf
 ("tu","spice","Turmeric","Holud","Curcuma longa","0910","Dried finger, powder","Middle East · UK · EU","",True),
 ("rc","spice","Dried red chilli","Shukna morich","Capsicum annuum","0904","Whole, powder","Middle East · UK","",False),
 ("co","spice","Coriander","Dhonia","Coriandrum sativum","0909","Seed, powder","Middle East · UK","",False),
 ("nc","spice","Black cumin (nigella)","Kalojira","Nigella sativa","0910","Seed, oil","Middle East · UK","",False),
 ("te","spice","Tea","Cha","Camellia sinensis","0902","CTC black, green, orthodox","Pakistan · UAE · UK","",False),
 ("bl","spice","Betel leaf","Paan","Piper betle","1404","Fresh leaf (air freight)","UK · Middle East","EU and UK apply import checks to betel leaf.",False),
 # ---- Fresh vegetables
 ("po","veg","Potato","Alu","Solanum tuberosum","0701","Table potato, 50 kg bags","Malaysia · Sri Lanka · Nepal · Middle East","",True),
 ("pt","veg","Pointed gourd","Potol","Trichosanthes dioica","0709","Fresh","UK · Middle East","",False),
 ("tg2","veg","Teasel gourd","Kakrol","Momordica dioica","0709","Fresh","UK · Middle East","",False),
 ("bg","veg","Bitter gourd","Korola","Momordica charantia","0709","Fresh","UK · Middle East · EU","",False),
 ("bt2","veg","Bottle gourd","Lau","Lagenaria siceraria","0709","Fresh","UK · Middle East","",False),
 ("ok","veg","Okra","Dherosh","Abelmoschus esculentus","0709","Fresh","UK · Middle East · EU","",False),
 ("bj","veg","Brinjal (aubergine)","Begun","Solanum melongena","0709","Fresh","UK · Middle East","",False),
 ("yb","veg","Yard-long bean","Borboti","Vigna unguiculata subsp. sesquipedalis","0708","Fresh","UK · Middle East","",False),
 ("ta","veg","Taro & arum","Kochu, mukhi kochu","Colocasia esculenta","0714","Fresh corms, stems","UK · Middle East","",False),
 ("gc","veg","Green chilli","Kacha morich","Capsicum annuum","0709","Fresh","UK · Middle East","",False),
 ("lg","veg","Leafy greens","Lal shak, pui shak","Amaranthus / Basella alba","0709","Fresh","UK · Middle East","",False),
 ("sk","veg","Shatkora citrus","Shatkora","Citrus macroptera","0805","Fresh","UK","Grown in Sylhet.",False),
 # ---- Fresh fruits
 ("mn","fruit","Mango (Himsagar, Langra, Amrapali, Fazli)","Aam","Mangifera indica","0804","Fresh, seasonal (May–August)","EU · UK · Middle East","",True),
 ("jf","fruit","Jackfruit","Kathal","Artocarpus heterophyllus","0810","Fresh, seasonal","UK · Middle East","",False),
 ("pa","fruit","Pineapple","Anarosh","Ananas comosus","0804","Fresh","Middle East · UK","",False),
 ("li","fruit","Lychee","Lichu","Litchi chinensis","0810","Fresh, seasonal (May–June)","Middle East · UK","",False),
 ("gv","fruit","Guava","Peyara","Psidium guajava","0804","Fresh","Middle East","",False),
 # ---- Frozen & ready-to-cook
 ("fv","frozen","Frozen vegetables","","Mixed vegetables","0710","IQF mixed, okra, beans, gourds","UK · Middle East · USA","",False),
 ("fp","frozen","Frozen paratha","Porota","Wheat flour","1905","Retail packs","UK · Middle East · USA · Canada","",False),
 ("fk","frozen","Frozen snacks (samosa, singara, spring roll)","","Assorted","1905 / 2106","Retail and food-service packs","UK · Middle East","",False),
 # ---- Processed & packaged
 ("bi","processed","Biscuits & bakery","","Wheat-based","1905","Retail packs, cartons","Middle East · Africa · UK · India","",False),
 ("nd","processed","Instant noodles","","Wheat-based","1902","Retail packs","Middle East · Africa · Asia","",False),
 ("sn","processed","Snacks (chanachur, chips)","Chanachur","Assorted","2106 / 2005","Retail packs","UK · Middle East · USA","",False),
 ("jc","processed","Fruit juices & drinks","","Mango, orange, litchi","2009 / 2202","PET, Tetra Pak, cans","Middle East · Africa · Asia","",False),
 ("pk","processed","Pickles & chutneys","Achar","Mango, olive, chilli","2001","Glass jars","UK · Middle East · USA","",False),
 ("sa","processed","Sauces & ketchup","","Tomato, chilli","2103","Bottles, sachets","Middle East · Africa","",False),
 ("sm","processed","Spice mixes (masala)","Moshla","Assorted spices","0910","Retail packs","UK · Middle East · USA","",False),
 ("mo2","processed","Mustard oil","Shorisha tel","Brassica juncea","1514","PET, tins","UK · Middle East","",False),
 ("hn","sweet","Honey (Sundarbans, mustard)","Modhu","Apis spp.","0409","Glass, PET","Middle East · UK","",False),
 ("jg","sweet","Date-palm jaggery","Khejur gur","Phoenix sylvestris","1702","Blocks, liquid (seasonal, December–February)","UK · Middle East · USA","HS heading to be confirmed per product form.",False),
]

# ---- Additional food & crop lines
P += [
 # Rice & grains
 ("kh","rice","Popped rice","Khoi","Oryza sativa","1904","Retail packs","UK · Middle East · USA","",False),
 ("rf","rice","Rice flour & pitha mixes","Chaler gura","Oryza sativa","1102 / 1901","Retail packs","UK · Middle East · USA","",False),
 # Spices, tea & leaf
 ("pp","spice","Panch phoron & whole spice blends","Panch phoron","Fenugreek, nigella, cumin, fennel, mustard","0910","Retail packs","UK · Middle East · USA","",False),
 ("gt2","spice","Green & organic tea","Sobuj cha","Camellia sinensis","0902","Loose leaf, tea bags","EU · USA · Japan · Middle East","Organic estates in Panchagarh and Sylhet.",False),
 # Fresh vegetables
 ("cb","veg","Cabbage & cauliflower","Bandhakopi, phulkopi","Brassica oleracea","0704","Fresh (winter season)","Malaysia · Singapore · Middle East · UK","",False),
 ("tm","veg","Tomato","Tomato","Solanum lycopersicum","0702","Fresh (winter season)","Middle East · Nepal","",False),
 ("pk2","veg","Pumpkin","Mishti kumra","Cucurbita moschata","0709","Fresh, whole","Middle East · Malaysia · UK","",False),
 ("ag","veg","Ash gourd","Chalkumra","Benincasa hispida","0709","Fresh","UK · Middle East","",False),
 ("sg","veg","Snake gourd","Chichinga","Trichosanthes cucumerina","0709","Fresh","UK · Middle East","",False),
 ("rg","veg","Ridge & sponge gourd","Jhinga, dhundul","Luffa acutangula / L. aegyptiaca","0709","Fresh","UK · Middle East","",False),
 ("ds2","veg","Drumstick","Sajna","Moringa oleifera","0709","Fresh pods","UK · Middle East","",False),
 ("gp2","veg","Green banana (plantain)","Kacha kola","Musa spp.","0803","Fresh","UK · Middle East","",False),
 ("gpa","veg","Green papaya","Kacha pepe","Carica papaya","0807","Fresh","UK · Middle East","",False),
 ("cl2","veg","Coriander leaves & herbs","Dhonepata","Coriandrum sativum","0709","Fresh bunches (air freight)","UK · Middle East","",False),
 ("lm","veg","Lemon & lime","Kagoji lebu","Citrus aurantiifolia","0805","Fresh","UK · Middle East","",False),
 # Fresh fruits
 ("bn","fruit","Banana","Kola (Sagor, Shabri)","Musa spp.","0803","Fresh","Middle East","",False),
 ("pw","fruit","Papaya (ripe)","Pepe","Carica papaya","0807","Fresh","Middle East · UK","",False),
 ("wm","fruit","Watermelon","Tormuj","Citrullus lanatus","0807","Fresh, seasonal (March–May)","Middle East","",False),
 ("cn","fruit","Green coconut","Daab","Cocos nucifera","0801","Fresh","Middle East · UK","",False),
 ("pm","fruit","Pomelo","Jambura","Citrus maxima","0805","Fresh, seasonal","UK · Middle East","",False),
 ("jj","fruit","Jujube","Boroi","Ziziphus mauritiana","0810","Fresh, seasonal (January–March)","Middle East · UK","",False),
 ("hp","fruit","Hog plum","Amra","Spondias pinnata","0810","Fresh, seasonal","UK · Middle East","",False),
 ("sf2","fruit","Star fruit","Kamranga","Averrhoa carambola","0810","Fresh","UK · Middle East","",False),
 ("wa2","fruit","Wood apple","Bel","Aegle marmelos","0810","Fresh, seasonal","UK · Middle East","",False),
 ("ol","fruit","Indian olive","Jolpai","Elaeocarpus serratus","0810","Fresh, seasonal (August–October)","UK · Middle East","",False),
 # Frozen & ready-to-cook
 ("fj","frozen","Frozen jackfruit (young & ripe)","Echor, kathal","Artocarpus heterophyllus","0811","IQF pieces, retail packs","UK · EU · USA","Young jackfruit is in demand as a plant-based meat alternative.",False),
 ("fu","frozen","Frozen puri, roti & pitha","","Wheat, rice flour","1905","Retail packs","UK · Middle East · USA","",False),
 ("fr","frozen","Frozen ready meals (biryani, curries)","","Assorted","1604 / 2106","Retail trays","UK · Middle East","Meat and fish meals need extra import approvals in most markets.",False),
 # Sugar & sweeteners
 ("cj","sweet","Cane jaggery","Akher gur","Saccharum officinarum","1701","Blocks","UK · Middle East","",False),
 ("ms","sweet","Molasses","Chitagur","Saccharum officinarum","1703","Bulk","Asia","",False),
 # Processed & packaged
 ("mp","processed","Mango pulp & purée","Aamer pulp","Mangifera indica","2008","Aseptic drums, cans","Middle East · EU · Asia","",False),
 ("cf","processed","Confectionery & candy","","Assorted","1704","Retail packs","Middle East · Africa · Asia","",False),
 ("rm","processed","Ready mixes (halim, kheer, firni)","","Assorted","1901","Retail packs","UK · Middle East · USA","",False),
 ("sw","processed","Traditional sweets (canned rasgulla, chomchom)","Mishti","Milk-based","0406 / 2106","Cans, tins","UK · Middle East · USA","Dairy products need a veterinary health certificate in most markets.",False),
 ("rbo","processed","Rice bran oil","Rice bran tel","Oryza sativa","1515","PET, tins","Asia","",False),
]

P += [
 ("bsc","shell","Blue swimming crab","Samudrik kakra","Portunus pelagicus","0306","Live, whole frozen, crab meat","China · Malaysia · Thailand · USA","",False),
 ("rr","rice","Red & brown rice","Lal chal","Oryza sativa","1006","Husked brown, red parboiled; 1–25 kg","UK · Middle East · USA","Export subject to current rice policy.",False),
]
