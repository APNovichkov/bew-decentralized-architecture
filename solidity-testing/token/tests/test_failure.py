def test_failed_assertion(accounts, token):
    balance = token.balanceOf(accounts[0])
    assert balance == 31337


def test_transaction_reverts(accounts, token):
    token.transfer(accounts[2], 10**18, {'from': accounts[1]})