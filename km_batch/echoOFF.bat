echo "1. This batch file shows the difference in how output looks with 'echo' et OFF"
python -V
echo "2. The prev command was 'python -V, and showed it printing the answer. Now repeating all these steps with echo OFF "
pause

echo OFF

echo "3. An echo statement before 'python -V' ."
python -V
echo "4. Done Running"
pause

echo "5. The above should have illustrated that echo OFF, the commands are not printed, only their outputs."
pause