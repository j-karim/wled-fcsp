# WLED goes FC St. Pauli
![FC St. Pauli Logo](resources/fcsp.svg)
Analogue push messages whenever FCSP scores! 
The most necessary [WLED](https://kno.wled.ge/) project you've seen so far. If you didn't know you needed it, now you know. 

## What does it do? 
Assuming you have a WLED LED strip (and you know the ip address), the code in this repo will make your LED strip shine (in FCSP colours) whenever Pauli scores (and it will flash for 10s if Pauli wins).

## What do you need? 
- One of
  - Python (and the requirements) installed
  - Docker
- A WLED LED strip (and its IP address)
- A football API key
  - There's a free basic plan (and I promise this repo does not need more than 100 requests per day)!
  - Get your API key [here](https://rapidapi.com/api-sports/api/api-football)
  - Important: This repo uses the rapidapi endpoints, please only get your API key from there

## Get started without docker 
Assuming you have python installed (e.g. via miniconda)
```
pip install -r requirements.txt
export IP_ADDRESS=<your_wled_ip_address_here>
export FOOTBALL_API_KEY=<your_rapid_api_key_here>
python -m wled_fcsp_controller.wled_control --ip_address=${IP_ADDRESS} --football_api_key=${FOOTBALL_API_KEY}
```

## Get started with docker 
Assuming you have python installed (e.g. via miniconda)
```
export IP_ADDRESS=<your_wled_ip_address_here>
export FOOTBALL_API_KEY=<your_rapid_api_key_here>
docker compose up --build 
```

This project was tested using `python=3.10`.

## Credits
- Have a look at the [WLED GitHub Repo](https://github.com/Aircoookie/WLED), it looks great.
- Have a look at the [Football API](https://www.api-football.com/)