:param url=>"https://vbatushkov.bitbucket.io/swapi.json";



// todo remove arrays / relationships from data that's set
CALL apoc.load.json($url) YIELD value
FOREACH (film in value.films | MERGE (f:Film { url: film.url }) ON CREATE SET f += film {.*, characters:null, planets:null, species:null,starships:null, vehicles:null})
FOREACH (character in value.people | MERGE (c:Character { url: character.url }) ON CREATE SET c += character {.*, species:null, vehicles:null, starships:null, films:null, homeworld:null} )
FOREACH (planet in value.planets | MERGE (p:Planet { url: planet.url }) ON CREATE SET p += planet {.*, residents:null, films:null} )
FOREACH (spec in value.species | MERGE (s:Species { url: spec.url }) ON CREATE SET s += spec {.*, films:null, people:null, homeworld:null})
FOREACH (vehicle in value.vehicles | MERGE (v:Vehicle { url: vehicle.url }) ON CREATE SET v += vehicle {.*, pilots:null, films:null} )
FOREACH (starship in value.starships | MERGE (s:Starship { url: starship.url }) ON CREATE SET s += starship {.*, pilots:null, films:null} )
;


CALL apoc.load.json($url) YIELD value
UNWIND value.films as film
UNWIND film.characters as character_url
MATCH (f:Film { url: film.url })
MATCH (c:Character { url: character_url })
MERGE (c)-[:APPEARED_IN]->(f);


CALL apoc.load.json($url) YIELD value
UNWIND value.films as film
UNWIND film.planets as planet_url
MATCH (f:Film { url: film.url })
MATCH (p:Planet { url: planet_url })
MERGE (p)-[:APPEARED_IN]->(f);

CALL apoc.load.json($url) YIELD value
UNWIND value.films as film
UNWIND film.species as species_url
MATCH (f:Film { url: film.url })
MATCH (spec:Species { url: species_url })
MERGE (spec)-[:APPEARED_IN]->(f);

CALL apoc.load.json($url) YIELD value
UNWIND value.films as film
UNWIND film.starships as starship_url
MATCH (f:Film { url: film.url })
MATCH (s:Starship { url: starship_url })
MERGE (s)-[:APPEARED_IN]->(f);

CALL apoc.load.json($url) YIELD value
UNWIND value.films as film
UNWIND film.vehicles as vehicle_url
MATCH (f:Film { url: film.url })
MATCH (v:Vehicle { url: vehicle_url })
MERGE (v)-[:APPEARED_IN]->(f);



CALL apoc.load.json($url) YIELD value
UNWIND value.people as character
UNWIND character.species as species_url
MATCH (c:Character { url: character.url })
MATCH (spec:Species { url: species_url })
MERGE (c)-[:OF]->(spec);

CALL apoc.load.json($url) YIELD value
UNWIND value.people as character
MATCH (c:Character { url: character.url })
MATCH (p:Planet { url: character.homeworld })
MERGE (c)-[:HOMEWORLD]->(p);

CALL apoc.load.json($url) YIELD value
UNWIND value.people as character
UNWIND character.vehicles as vehicle_url
MATCH (c:Character { url: character.url })
MATCH (v:Vehicle { url: vehicle_url })
MERGE (c)-[:PILOT]->(v);


CALL apoc.load.json($url) YIELD value
UNWIND value.people as character
UNWIND character.starships as starship_url
MATCH (c:Character { url: character.url })
MATCH (s:Starship { url: starship_url })
MERGE (c)-[:PILOT]->(s);


CALL apoc.load.json($url) YIELD value
UNWIND value.species as species
MATCH (spec:Species { url: species.url })
MATCH (p:Planet { url: species.homeworld })
MERGE (spec)-[:HOMEWORLD]->(p);

MATCH (s:Species) SET  s.real_average_height=s.average_height;

MATCH (s:Starship {name:"Sentinel-class landing craft"}) set s.realHeight = 2900, s.height = 29 ;
MATCH (s:Starship {name:"Death Star"}) set s.realHeight = 12000000, s.height = 120000000;
MATCH (s:Starship {name:"Millennium Falcon"}) set s.realHeight = 780, s.height = 78 ;
MATCH (s:Starship {name:"Y-wing"}) set s.realHeight = 244, s.height = 244 ;
MATCH (s:Starship {name:"X-wing"}) set s.realHeight = 240, s.height = 240 ;
MATCH (s:Starship {name:"TIE Advanced x1"}) set s.realHeight = 380, s.height = 380 ;
MATCH (s:Starship {name:"Executor"}) set s.realHeight = 126700, s.height = 126700 ;
MATCH (s:Starship {name:"Slave 1"}) set s.realHeight = 2150, s.height = 2150 ;
MATCH (s:Starship {name:"Imperial shuttle"}) set s.realHeight = 2265, s.height = 2265 ;
MATCH (s:Starship {name:"EF76 Nebulon-B escort frigate"}) set s.realHeight = 16600, s.height = 16600 ;
MATCH (s:Starship {name:"Calamari Cruiser"}) set s.realHeight = 15000, s.height = 15000 ;
MATCH (s:Starship {name:"A-wing"}) set s.realHeight = 247, s.height = 247 ;
MATCH (s:Starship {name:"B-wing"}) set s.realHeight = 250, s.height = 250;
MATCH (s:Starship {name:"Republic Cruiser"}) set s.realHeight = 26800, s.height = 26.800 ;
MATCH (s:Starship {name:"Naboo fighter"}) set s.realHeight = 2500, s.height = 25 ;
MATCH (s:Starship {name:"Naboo Royal Starship"}) set s.realHeight = 150, s.height = 150 ;
MATCH (s:Starship {name:"Scimitar"}) set s.realHeight = 1250, s.height = 1250 ;
MATCH (s:Starship {name:"J-type diplomatic barge"}) set s.realHeight = 370, s.height = 370 ;
MATCH (s:Starship {name:"AA-9 Coruscant freighter"}) set s.realHeight = 7000, s.height = 7000 ;
MATCH (s:Starship {name:"Jedi starfighter"}) set s.realHeight = 244, s.height = 24.4 ;
MATCH (s:Starship {name:"H-type Nubian yacht"}) set s.realHeight = 710, s.height = 710 ;
MATCH (s:Starship {name:"Star Destroyer"}) set s.realHeight = 26800, s.height = 26800 ;
MATCH (s:Starship {name:"Trade Federation cruiser"}) set s.realHeight = 102877, s.height = 102877 ;
MATCH (s:Starship {name:"Theta-class T-2c shuttle"}) set s.realHeight = 18500, s.height = 18500 ;
MATCH (s:Starship {name:"T-70 X-wing fighter"}) set s.realHeight = 240, s.height = 24 ;
MATCH (s:Starship {name:"Rebel transport"}) set s.realHeight = 500, s.height = 500 ;
MATCH (s:Starship {name:"Droid control ship"}) set s.realHeight = 102877, s.height = 102877  ;
MATCH (s:Starship {name:"Republic Assault ship"}) set s.realHeight = 20000, s.height = 20000 ;
MATCH (s:Starship {name:"Solar Sailer"}) set s.realHeight = 480, s.height = 480 ;
MATCH (s:Starship {name:"Republic attack cruiser"}) set s.realHeight = 26800, s.height = 26800 ;
MATCH (s:Starship {name:"Naboo star skiff"}) set s.realHeight = 300, s.height = 300 ;
MATCH (s:Starship {name:"Jedi Interceptor"}) set s.realHeight = 250, s.height = 250 ;
MATCH (s:Starship {name:"arc-170"}) set s.realHeight = 381, s.height = 381 ;
MATCH (s:Starship {name:"Banking clan frigte"}) set s.realHeight = 24300, s.height = 24300 ;
MATCH (s:Starship {name:"Belbullab-22 starfighter"}) set s.realHeight = 300, s.height = 30 ;
MATCH (s:Starship {name:"V-wing"}) set s.realHeight = 584, s.height = 584 ;
MATCH (s:Starship {name:"CR90 corvette"}) set s.realHeight = 3260, s.height = 3260 ;
MATCH (s:Species {name:"Hutt"}) set s.average_height=600;
MATCH (s:Species {name:"Yoda's species"}) set s.average_height=66;
MATCH (s:Species {name:"Trandoshan"}) set s.average_height=200;
MATCH (s:Species {name:"Mon Calamari"}) set s.average_height=160;
MATCH (s:Species {name:"Ewok"}) set s.average_height=100;
MATCH (s:Species {name:"Sullustan"}) set s.average_height=180;
MATCH (s:Species {name:"Neimodian"}) set s.average_height=180;
MATCH (s:Species {name:"Gungan"}) set s.average_height=190;
MATCH (s:Species {name:"Toydarian"}) set s.average_height=120;
MATCH (s:Species {name:"Dug"}) set s.average_height=100;
MATCH (s:Species {name:"Twi'lek"}) set s.average_height=200;
MATCH (s:Species {name:"Aleena"}) set s.average_height=80;
MATCH (s:Species {name:"Vulptereen"}) set s.average_height=1000;
MATCH (s:Species {name:"Xexto"}) set s.average_height=125;
MATCH (s:Species {name:"Toong"}) set s.average_height=200;
MATCH (s:Species {name:"Cerean"}) set s.average_height=800;
MATCH (s:Species {name:"Nautolan"}) set s.average_height=180;
MATCH (s:Species {name:"Zabrak"}) set s.average_height=180;
MATCH (s:Species {name:"Tholothian"}) set s.average_height=0;
MATCH (s:Species {name:"Iktotchi"}) set s.average_height=180;
MATCH (s:Species {name:"Quermian"}) set s.average_height=240;
MATCH (s:Species {name:"Kel Dor"}) set s.average_height=180;
MATCH (s:Species {name:"Chagrian"}) set s.average_height=190;
MATCH (s:Species {name:"Geonosian"}) set s.average_height=178;
MATCH (s:Species {name:"Mirialan"}) set s.average_height=180;
MATCH (s:Species {name:"Clawdite"}) set s.average_height=180;
MATCH (s:Species {name:"Besalisk"}) set s.average_height=178;
MATCH (s:Species {name:"Kaminoan"}) set s.average_height=220;
MATCH (s:Species {name:"Skakoan"}) set s.average_height=0;
MATCH (s:Species {name:"Muun"}) set s.average_height=190;
MATCH (s:Species {name:"Togruta"}) set s.average_height=180;
MATCH (s:Species {name:"Kaleesh"}) set s.average_height=170;
MATCH (s:Species {name:"Pau'an"}) set s.average_height=190;
MATCH (s:Species {name:"Wookiee"}) set s.average_height=210;
MATCH (s:Species {name:"Droid"}) set s.average_height=0;
MATCH (s:Species {name:"Human"}) set s.average_height=680;
MATCH (s:Species {name:"Rodian"}) set s.average_height=170;
MATCH (a) SET a.updated=False; 
MATCH (a)-[r]-(b) SET r.deleted=false, r.updated=False, r.toDelete=False;
MATCH (c:Character {name:"Anakin Skywalker"}), (s:Starship {name:"Death Star"}) merge (c)-[:PILOT {toDelete:True, deleted:false, updated:False}]->(s);
MATCH (c:Character {name:"Darth Maul"}), (s:Vehicle {name:"Snowspeeder"}) merge (c)-[:PILOT {toDelete:True, deleted:false,  updated:False}]->(s);
MATCH (c:Character {name:"Anakin Skywalker"}), (s:Vehicle {name:"T-16 skyhopper"}) merge (c)-[:PILOT {toDelete:True, deleted:false,  updated:False}]->(s);
MATCH (c:Character {name:"Dormé"}), (s:Starship {name:"Millennium Falcon"}) merge (c)-[:PILOT {toDelete:True, deleted:false,  updated:False}]->(s);
MATCH (c:Character {name:"Finn"}), (s:Starship {name:"Naboo fighter"}) merge (c)-[:PILOT {toDelete:True, deleted:false,  updated:False}]->(s);



MATCH (a:Character)-[p:PILOT {deleted:false}]->(b:Starship)-[r:APPEARED_IN {deleted:false}] ->(c:Film) WHERE not (a)-[:APPEARED_IN {deleted:false}]->(c) MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:0})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c);
MATCH (a:Character)-[p:PILOT {deleted:false}]->(b:Vehicle)-[r:APPEARED_IN {deleted:false}] ->(c:Film) WHERE not (a)-[:APPEARED_IN {deleted:false}]->(c) MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:1})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c);
MATCH (a:Species)<-[p:OF {deleted:false}]-(b:Character)-[r:PILOT {deleted:false}]->(c:Starship) WHERE a.average_height>c.height MERGE (a)-[:BELONGS]->(v1:Violation {solved:false, locked:false, nodes: ID(a)+','+ID(b)+','+ID(c)+','+ID(p)+','+ID(r),labels:'a,b,c,p,r', type:2})<-[:BELONGS]-(b) MERGE (v1)<-[:BELONGS]-(c);
MATCH (v1:Violation)<-[:BELONGS]-(a)-[:BELONGS]->(v2:Violation) WHERE id(v1)<>id(v2) and not (v1)-[:INTERSECT]-(v2) merge (v1)-[:INTERSECT]-(v2);
