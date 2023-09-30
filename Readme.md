# BlockChain Assignment
## Group Details:
### Rohan Chavan         2021A7PS2739H
### Kshitiz Agarwal      2021A7PS1818H 
### Subal Tankwal        2021A7PS1407H 
### Sparsh Khandelwal    2021A7PS1320H 
### Vansh Gupta          2021A7PS2615H 
## final file:
## Class BlockChain:
 ### create_user
  This creates a new user, a user created can be distributor or client which is decided by the input given by the user 
  if user enters 1 the user is dis and 0 when user is client 
  once called this function take some information of the user which are stated below:
    1- user id 
    2- user name
    3- stake of the user


 ### Create_block
   This creates a new block and adds it in the merkle tree. Transactions are added to block when thy are in a multiple of 3.
 ### create_transaction
  This function takes the buyer id, seller id, product id and number of products. The transaction created is between a distributor and a client.
  The transaction also stores the time of transaction. Also it takes the signature of the sender.
 ### create_transaction_as_a_manufacture
  This function creates a transaction between manufacturer and distributor. It takes receiver id, product id and units as input since we know that the sender is manufacturer and there is only 1 manufacturer.
 ### validate_transaction
 This checks for any wrong transactions like selling to yourself or a client selling to someone. 
 ### validate_chain
 
 ### print_blockchain
 ### print_product_history
 ### generate_QR_Code
 ### hash
 ### create_timer
 ### print_nodes
<br>

## merkle_tree file:

