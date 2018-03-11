# distributed-group-messenger
Group messenger in distributed nodes.

Δουλεύει με software multicast. Υπάρχει πρόβλημα στο ότι δεν ενημερόνεται ένας client για νέα μέλη στο γκρουπ.(late joiner πρόβλημα).

Έχει υλοποιηθεί με select και για παραλαβή μηνύματα και για εισαγωγή input. 

Πρόβλημα: Αν έρθει μήνυμα καθώς γράφουμε μία εντολή στο τερματικό. Τότε ο buffer κρατάει αυτά γράφαμε αλλά δεν τα εμφανίζει μετά το μήνυμα.

Πρώτη προτεραιότητα το ordering FIFO και Total ξεχωριστά.
To total ordering γνεται με δύο τρόπους:
 -sequencer (Τρέχει σε ένα server)
 -ISIS (κατανεμημένος αλγόριθμος)


## Giorgos: 
  - !w fix
  - λύση για το late joiner 
## Manolis:
  - Heartbeats 
  - ordering
## Panagiotis:
  - ordering
  
  
### Ordering links

[FIFO και total ordering μαζί](https://github.com/ramanpreetSinghKhinda/CSE_586_Group_Messenger_TOTAL_FIFO_Ordering/blob/master/GroupMessenger2/app/src/main/java/edu/buffalo/cse/cse486586/groupmessenger2/GroupMessengerActivity.java)

[total ordering ISIS C++](https://github.com/shamirwa/ISIS---Total-Order-Multicast-Algorithm)

[total ordering ISIS C++](https://github.com/hikushalhere/IsisTotalOrderMulticast)

[total ordering Sequencer python](https://github.com/evapujals/GroupCast)

## Άλλα repos
[Total ordering ISIS](https://github.com/search?utf8=%E2%9C%93&q=total+ordering+ISIS&type=)

[Total ordering python](https://github.com/search?l=Python&q=total+ordering&type=Repositories&utf8=%E2%9C%93)

