curl -X POST cartoku:8000/wadus/apps -d name=dummy -d description="dewfre frelfk jreflrekjf lrekj"
curl cartoku:8000/wadus/apps | python3 -m json.tool
curl cartoku:8000/wadus/apps/dummy | python3 -m json.tool
curl cartoku:8000/wadus/apps/dummy/deploys | python3 -m json.tool
curl cartoku:8000/wadus/apps/dummy/deploys/1 | python3 -m json.tool
