# WLED goes FC St. Pauli
![FC St. Pauli Logo](resources/fcsp.svg)
Analogue push messages whenever FCSP scores! 
The most necessary [WLED](https://kno.wled.ge/) project you've seen so far. If you didn't know you needed it, now you know. 

## What does it do? 
Assuming you have a WLED LED strip (and you know the ip address), the code in this repo will make your LED strip shine (in FCSP colours) whenever Pauli scores.

## What do you need? 
- One of
  - Python (and the requirements) installed
  - Docker
- A WLED LED strip (and its IP address)


## Get started without docker 
Assuming you have python installed (e.g. via miniconda)
```
pip install -r requirements.txt
python -m wled_fcsp_controller.wled_control --ip_address=<your_wled_ip_address_here>
```

## Get started with docker 
Assuming you have python installed (e.g. via miniconda)
```
export IP_ADDRESS=<your_wled_ip_address_here>
docker compose up --build 
```

This project was tested using `python=3.10`.

## Credits
- Have a look at the [WLED GitHub Repo](https://github.com/Aircoookie/WLED), it looks great.