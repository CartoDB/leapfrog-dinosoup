curl -X POST carto.ku/wadus/apps -d name=dummy -d description="dewfre frelfk jreflrekjf lrekj"
curl carto.ku/wadus/apps | python3 -m json.tool
curl carto.ku/wadus/apps/dummy | python3 -m json.tool
curl carto.ku/wadus/apps/dummy/deploys | python3 -m json.tool
curl carto.ku/wadus/apps/dummy/deploys/1 | python3 -m json.tool
