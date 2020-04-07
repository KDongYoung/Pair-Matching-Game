# Pair-Matching-Game
Basic Pair Matching game + can find the rank of the game result (found by server connection))
--------------------------------------------------------------------------
# [ GUI ]




--------------------------------------------------------------------------
# [ HOW TO RUN  ] 
1. Download 'SQlite' and save it in C drive. Name the folder ‘sqlite’.
2. Run ‘1. Database’ (create 'pairgameDB' database, create 'pairgame' table)
<div>
  <img src="https://user-images.githubusercontent.com/37610908/78502157-8cda3100-779a-11ea-81ac-abc1b0033630.jpg" width="150%"></img>
</div>

3. Change the IP variable value as the IP address which the user will use as a main server in file ‘2_1. client’ line 403.
<div>
  <img src="https://user-images.githubusercontent.com/37610908/78502155-8b106d80-779a-11ea-8f71-4c0027f8f3be.jpg" width="80%" height="60%"></img>
</div>

4. Run ‘2_1. server’ (don't stop running, make it active until the user stops playing)
5. Run ‘2_2. client’ and start playing.

# [ USED MODULE / REQUIREMENT ] 
for GUI : tkinter, threading, random
for server, client : sys, socket, threading
<div>
  <img src="https://user-images.githubusercontent.com/37610908/78502158-8d72c780-779a-11ea-901a-bfd5bcb3e97d.jpg" width="30%"></img>
  <img src="https://user-images.githubusercontent.com/37610908/78502159-8e0b5e00-779a-11ea-8a8b-eb63b7bac958.jpg" width="30%"></img>
</div>
