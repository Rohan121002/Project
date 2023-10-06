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

# blockchain.py File:
## Class BlockChain:
 ### create_user:
  This creates a new user, a user created can be distributor or client which is decided by the input given by the user 
  if user enters 1 the user is dis and 0 when user is client 
  once called this function take some information of the user which are stated below:<br> 
    1- user id <br>
    2- user name<br>
    3- stake of the user<br>


 ### create_new_block:
   This creates a new block. Transactions are added to block when thy are in a multiple of 3. It creates a header which includes an index, timestamp, previous hash, and merkle root.
 ### create_transaction:
  This function is essencially used to create a transaction. The traansaction done is this fucntion is only between distributor and client. 
  It takes following inputs to create a transaction:<br>
    1- buyer id<br>
    2- seller id<br>
    3- product id<br>
    4 number of product<br>

  It takes the disributor's verdict where he is initiating the transaction with sign or wothout sigh
  We also do the lie detection in this function which is as follows:<br>
    1 if client verdict is YES which means he as received the transaction and at this point there is also distributor signature on transaction then the transaction is successfully executed.<br>
    2 if above is not true and client verdict is No and signature is present then client is lying and hence the stakes fo client would be reduced.<br>
    3 if above all are not true and client verdict is NO and there is no distributor signature then the seller is lying and hence stakes of buyer are reduced <br>
    
   if successfully completing the transaction if the total number of transaction in the transaction list is multiple of 3 than the block is given to mine 
 ### create_transaction_as_a_manufacture:
  This function creates a transaction between manufacturer and distributor. It takes receiver id, product id and units as input since we know that the sender is manufacturer and there is only 1 manufacturer.
 ### validate_transaction:
 This checks for any wrong transactions like selling to yourself or a client selling to someone. 
 ### validate_chain:
 This function verifies whether the blockchain is valid one or not. If the hash value contained in header of the current block is not same as hash of the previous block, then this function returns false otherwise it returns true and the other functions continue to execute. 
 ### print_blockchain:
 This function prints all the blocks created till that time in the blockchain i.e. their block number, header of each block and the transactions associated with that particular block.
 ### print_product_history:
 To print all the transaction details, this function is used. It prints the name of the seller and buyer, how many units bought, product ID of that product, buying time and receiving time. 
 ### generate_QR_Code:
 Whatever the information is stored in the product_history part of the program is represented in the form of QR Code using this functionality which can be scanned to read all the details. Feature 4 is implemented using this function.
 ### hash:
 This function takes 'block' as the input and creates the hash value of the input. The input can be any transaction, a whole block, or merkle tree. 
 ### create_timer:
 This functions implements the actual consensus algorithm by allowing the person with the highest number of stakes to be the miner. For this, we calculate the total number of stakes of all the user, then double it and divide by the number of users.
Then we create a randomize function ranging between 1 and the above value to add this value to their individual stakes. Hence, each user has the chance to become miner with some probability
At the end, the user with the highest stakes will mine the block and stakes for rest of the users will remain as it is.
 ### print_nodes:
 This function prints information of all the users in the blockchain like his ID,name,product ID,number of products owned and total stakes. This also displays whether an user is a manufacturer, distributor or client.
<br>

# merkle_tree.py file:

## Class Node:
 defines a node with left, right and a value
### Class MerkleTree: 
#### hash: 
returns SHA256 encoded value
#### buildTree:
recursive function to create the tree
#### getRootHash:
returns root value