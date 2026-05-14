import unittest
from bank_simulation import BankSimulation


class UnitTests(unittest.TestCase):
    def test_01(self):
        s = BankSimulation()
        self.assertTrue(s.create_account(1,'acc0'))
        self.assertTrue(s.create_account(2,'acc1'))
        self.assertTrue(s.create_account(3,'acc2'))
        self.assertTrue(s.create_account(4,'acc3'))
        self.assertTrue(s.create_account(5,'acc4'))
        self.assertTrue(s.create_account(6,'acc5'))
        self.assertTrue(s.create_account(7,'acc6'))
        self.assertTrue(s.create_account(8,'acc7'))
        self.assertTrue(s.create_account(9,'acc8'))
        
        self.assertEqual(s.deposit(10,'acc0',6912),6912)
        self.assertEqual(s.deposit(11,'acc1',3946),3946)
        self.assertEqual(s.deposit(12,'acc2',6179),6179)
        self.assertEqual(s.deposit(13,'acc3',5366),5366)
        self.assertEqual(s.deposit(14,'acc4',6500),6500)
        self.assertEqual(s.deposit(15,'acc5',4672),4672)
        self.assertEqual(s.deposit(16,'acc6',5000),5000)
        self.assertEqual(s.deposit(17,'acc7',6902),6902)
        self.assertEqual(s.deposit(18,'acc8',4018),4018)
        
        self.assertEqual(s.transfer(19,'acc0', 'acc1', 1757),'transfer1')
        self.assertEqual(s.transfer(20,'acc1', 'acc0', 2018),'transfer2')
        self.assertEqual(s.transfer(21,'acc2', 'acc0', 2945),'transfer3')
        self.assertEqual(s.transfer(22,'acc3', 'acc1', 3672),'transfer4')
        self.assertEqual(s.transfer(23,'acc4', 'acc2', 4752),'transfer5')
        self.assertEqual(s.transfer(24,'acc5', 'acc3', 2482),'transfer6')
        self.assertEqual(s.transfer(25,'acc6', 'acc4', 2387),'transfer7')
        self.assertEqual(s.transfer(26,'acc7', 'acc5', 2728),'transfer8')
        self.assertEqual(s.transfer(27,'acc8', 'acc6', 1211),'transfer9')
        
        self.assertEqual(s.pay(19,'acc0',887),6025)
        self.assertEqual(s.pay(20,'acc1',1721),2225)
        self.assertEqual(s.pay(21,'acc2',583),5596)
        self.assertEqual(s.pay(22,'acc3',1622),3744)
        self.assertEqual(s.pay(23,'acc4',1292),5208)
        self.assertEqual(s.pay(24,'acc5',1511),3161)
        self.assertEqual(s.pay(25,'acc6',1159),3841)
        self.assertEqual(s.pay(26,'acc7',1036),5866)
        self.assertEqual(s.pay(27,'acc8',982),3036)
        
        self.assertIsNone(s.pay(28,'acc1',9999))
        self.assertIsNone(s.pay(29,'non-existing',500))
        
        top_activity = ['acc4(12544)', 'acc7(10666)', 'acc3(10660)', 
                        'acc2(9707)', 'acc0(9556)', 'acc5(8665)', 
                        'acc6(8546)']
        
        self.assertEqual(s.top_activity(39,7),top_activity)
        
        self.assertFalse(s.accept_transfer(40,'acc1','non-existing'))
        self.assertTrue(s.accept_transfer(86400041,'acc1','transfer1'))
        self.assertTrue(s.accept_transfer(86400042,'acc0','transfer2'))
        self.assertTrue(s.accept_transfer(86400043,'acc0','transfer3'))
        self.assertTrue(s.accept_transfer(86400044,'acc1','transfer4'))
        self.assertTrue(s.accept_transfer(86400045,'acc2','transfer5'))
        self.assertTrue(s.accept_transfer(86400046,'acc3','transfer6'))
        self.assertTrue(s.accept_transfer(86400047,'acc4','transfer7'))
        self.assertTrue(s.accept_transfer(86400048,'acc5','transfer8'))
        self.assertTrue(s.accept_transfer(86400049,'acc6','transfer9'))
        
    
    def test_02(self):
        s = BankSimulation()
        
        # 1. Setup Phase: Create accounts and initial funding
        self.assertTrue(s.create_account(100, "Alice"))
        self.assertTrue(s.create_account(200, "Bob"))
        self.assertEqual(s.deposit(300, "Alice", 1000), 1000)
        
        # 2. Transfer Phase: Alice sends money to Bob
        # This should subtract 500 from Alice immediately
        t_id = s.transfer(400, "Alice", "Bob", 500)
        self.assertEqual(t_id, "transfer1")
        self.assertEqual(s.accounts["Alice"].balance, 500)
        self.assertEqual(s.accounts["Bob"].balance, 0) # Bob hasn't accepted yet!

        # 3. Acceptance Phase: Bob accepts the transfer
        # Bob's balance should now reflect the 500
        self.assertTrue(s.accept_transfer(500, "Bob", t_id))
        self.assertEqual(s.accounts["Bob"].balance, 500)

        # 4. Activity Check: Who is the most active?
        # Alice spent 1000 (deposit) + 500 (transfer) = 1500
        # Bob received 500 (transfer deposit) = 500
        expected_activity = ["Alice(1500)", "Bob(500)"]
        self.assertEqual(s.top_activity(600, 2), expected_activity)

        # 5. Expiration Phase: Alice tries to send money again, but Bob waits too long
        # Current timestamp: 1000. Expiration: 1000 + 86,400,000
        t_id_expired = s.transfer(1000, "Alice", "Bob", 100)
        self.assertEqual(s.accounts["Alice"].balance, 400) # Money taken upfront
        
        # Fast forward time past 24 hours (86,400,000 ms)
        expiry_time = 1000 + 86400000 + 1 
        
        # Bob tries to accept, but it's too late. 
        # The function should return False and Alice should be refunded.
        self.assertFalse(s.accept_transfer(expiry_time, "Bob", t_id_expired))
        self.assertEqual(s.accounts["Alice"].balance, 500) # Refunded!

        # 6. Edge Case: Transfer to self or non-existent account
        self.assertIsNone(s.transfer(2000, "Alice", "Alice", 10))
        self.assertIsNone(s.transfer(2000, "Alice", "NonExistent", 10))
        

if __name__ == "__main__":
    unittest.main()