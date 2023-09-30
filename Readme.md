# BlockChain Assignment
## Group Details:
### Rohan Chavan         2021A7PS2739H
### Kshitiz Agarwal      2021A7PS1818H 
### Subal Tankwal        2021A7PS1407H 
### Sparsh Khandelwal    2021A7PS1320H 
### Vansh Gupta          2021A7PS2615H 

# Features in this project: 
1.  Register new clients, distributors: **create_user** function
2.  POS concensus algorithm implemented : **create_timer** function *line 340*
3. Implemented merkle tree to calculate hash : **merkle tree file**
4. View current product status using QRcode : **generate_QR_Code** and *pyqrcode* library
5. Create transaction from distributor to client: **create_transaction**
6. Lie detection: whether distributor or client is lying or not. If yes then deduct from security deposit: **create_transaction** function
## final file:
## Class BlockChain:
 ### create_user
  This creates a new user, a user created can be distributor or client which is decided by the input given by the user 
  if user enters 1 the user is dis and 0 when user is client 
  once called this function take some information of the user which are stated below:
    1- user id 
    2- user name
    3- stake of the user


 ### create_new_block
   This creates a new block. Transactions are added to block when thy are in a multiple of 3. It creates a header which includes an index, timestamp, previous hash, and merkle root.
 ### create_transaction
  This function is essencially used to create a transaction. The traansaction done is this fucntion is only between distributor and client. 
  It takes following inputs to create a transactuion:
    1 buyer id
    2 seller id
    3 product id
    4 number of product
  It takes the disributor's verdict where he is initiating the transaction with sign or wothout sigh
  We also do the lie detection in this function which is as follows:
    1 if client verdict is YES which means he as received the transaction and at this point there is also distributor signature on transaction then the transaction is successfully executed
    2 if above is not true and client verdict is No and signature is present then client is lying and hence the stakes fo client would be reduced
    3 if above all is not true and client verdict is NO and there is no distributor signature than the seller is lying ans hence stakes of buyer are reduced 
  if successfully completing the transaction if the total number of transaction in the transaction list is multiple of 3 than the block is given to mine
  <!-- This function takes the buyer id, seller id, product id and number of products. The transaction created is between a distributor and a client.
  The transaction also stores the time of transaction. Also it takes the signature of the sender.
  This function implements the lie detection feature. -->
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

### Class Node:
 defines a node with left, right and a value
### Class MerkleTree: 
#### hash : 
returns SHA256 encoded value
#### buildTree:
recursive function to create the tree
#### getRootHash
returns root value