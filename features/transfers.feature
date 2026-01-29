Feature: Transfers

Scenario: User is able to receive money
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    And Account with pesel "95092909876" has "balance" equal to "0.0"
    And User with pesel "95092909876" makes "incoming" transfer with value "100"
    Then Account with pesel "95092909876" has "balance" equal to "100.0"

Scenario: User won't receive negative amount
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    And Account with pesel "95092909876" has "balance" equal to "0.0"
    And User with pesel "95092909876" makes "incoming" transfer with value "-20"
    Then Account with pesel "95092909876" has "balance" equal to "0.0"

Scenario: User can send the money
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    And User with pesel "95092909876" makes "incoming" transfer with value "20"
    And Account with pesel "95092909876" has "balance" equal to "20.0"
    And User with pesel "95092909876" makes "outgoing" transfer with value "15"
    Then Account with pesel "95092909876" has "balance" equal to "5.0"

Scenario: User can't send more than balance
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    And User with pesel "95092909876" makes "incoming" transfer with value "20"
    And Account with pesel "95092909876" has "balance" equal to "20.0"
    And User with pesel "95092909876" makes "outgoing" transfer with value "30"
    Then Account with pesel "95092909876" has "balance" equal to "20.0"

Scenario: User can't send negative value
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    And User with pesel "95092909876" makes "incoming" transfer with value "20"
    And Account with pesel "95092909876" has "balance" equal to "20.0"
    And User with pesel "95092909876" makes "outgoing" transfer with value "-5"
    Then Account with pesel "95092909876" has "balance" equal to "20.0"