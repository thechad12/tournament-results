# tournament-results

Prerequisites: The latest version of vagrant 

Instructions: 
  1. Start vagrant by opening the terminal or cmd and browse to the vagrant folder, then type vagrant up.
  2. Type vagrant ssh to login to the vagrant machine.
  3. Change to the correct folder - cd /vagrant/tournament.
  4. Type 'psql tournament < tournament.sql' to import the sql commands.
  5. To run the tests, type 'python tournament_test.py.'
