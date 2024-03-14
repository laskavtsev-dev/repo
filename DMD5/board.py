from smbus import SMBus
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
 
app = FastAPI()
bus = SMBus(1)
sensorAddress = 0x23
class Zone(BaseModel):
    text: str
    brt: int
    addr: int
 
dataset = {
    0: Zone(text="", brt=127, addr=8),
    1: Zone(text="", brt=127, addr=9),
    2: Zone(text="", brt=127, addr=10),
    3: Zone(text="", brt=127, addr=11),
    4: Zone(text="", brt=127, addr=12),
}
 
def Display(
    txt: str,
    brt: int,
    addr: int,
    ):
    tempString = str(brt) + "~" + txt
    textToSend = []
    for c in tempString:
        textToSend.append(ord(c))
 
    bus.write_i2c_block_data(addr,0x01,textToSend)
 
@app.get("/")
def index() -> dict[str, dict[int, Zone]]:
    return {dataset}
 
@app.get("/zone/{zone_id}")
def query_zone_by_id(zone_id: int) -> Zone:
    if zone_id not in dataset:
        raise HTTPException(
            status_code=404, detail=f"Zone with id {zone_id} does not exist!"
        )
    return dataset[zone_id]
 
@app.put("/payload")
async def payload(data: Request):
    received = await data.json()
    brightness = bus.read_byte_data (sensorAddress, 0x01)
    if len(received) > len(dataset):
        finish = len(dataset) 
        excessive = {value[0]:value[1] for key, value in enumerate(received.items()) if key >= finish}
    else:
        finish = len(received)
        excessive = {}
    for i in range(0,finish):
        zone = dataset[i]
        zone.text = received[f"{str(i)}"]
        zone.brt = brightness
        Display(zone.text[:10], zone.brt, zone.addr)
    return excessive