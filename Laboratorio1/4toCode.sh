mkdir -p "Designed tasks"/{"Maintenance","Production Line","Fixes","Costs"}
touch "Designed tasks"/{"Maintenance/dates","Production Line/dates","Fixes/dates","Costs/dates"}
echo "Maintenance - Monday" > "Designed tasks/Maintenance/dates"
echo "Production line – Tuesday" > "Designed tasks/Production Line/dates"
echo "Fixes – Wendsday" > "Designed tasks/Fixes/dates"
echo "Costs – Friday" > "Designed tasks/Costs/dates"
tree "Designed tasks"

