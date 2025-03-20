sudo adduser company
sudo usermod -aG sudo company
sudo adduser engineer
sudo adduser operator1
sudo groupadd --force Distibution
sudo usermod -aG Distribution company
sudo usermod -aG Distribution engineer
sudo usermod -aG Distribution operator1
