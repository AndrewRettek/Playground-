## testcases.rpy - Automated test cases for BindrChat
##
## Run all tests:  renpy.exe "C:/Users/andre/Playground-" test
## Run one test:   renpy.exe "C:/Users/andre/Playground-" test smoke_test
##
## The test runner opens a window and drives the UI autonomously.
## Output shows PASSED/FAILED. After the test finishes, the game window
## stays open — kill the process afterward (the run_tests.sh wrapper
## handles this automatically).
##
## If the proxy server is unreachable, the game handles it gracefully
## (shows an error message bubble), so tests won't crash.

## Give tests enough time for screen transitions and potential API calls
define _test.timeout = 10.0


## ===================================================================
## SMOKE TEST - Basic navigation: Start -> Messages -> Open chat -> Back
## ===================================================================

testcase smoke_test:
    ## Main menu -> click Start
    click "Start"
    pause 1.0

    ## Messages screen should be showing all character contacts
    ## Open Mallory's chat
    click "Mallory"
    pause 1.0

    ## Chat screen loaded -- go back to messages
    click "Back"
    pause 1.0

    ## Open a different character
    click "Rye"
    pause 1.0

    ## Back to messages list
    click "Back"
    pause 1.0


## ===================================================================
## ALL CONTACTS LOAD - Verify every character's chat screen opens
## ===================================================================

testcase all_contacts_load:
    click "Start"
    pause 1.0

    ## Mallory
    click "Mallory"
    pause 1.0
    click "Back"
    pause 1.0

    ## Rye
    click "Rye"
    pause 1.0
    click "Back"
    pause 1.0

    ## Demitria
    click "Demitria"
    pause 1.0
    click "Back"
    pause 1.0

    ## Gabby
    click "Gabby"
    pause 1.0
    click "Back"
    pause 1.0


## ===================================================================
## SEND MESSAGE - Type a message and send it
## ===================================================================

testcase send_message:
    click "Start"
    pause 1.0

    ## Open Mallory's chat
    click "Mallory"
    pause 1.0

    ## Type a message into the input field
    type "Hello from the test runner"
    pause 0.5

    ## Press Enter to send (triggers input_enter key binding)
    keysym "K_RETURN"

    ## Wait for API response (server may be offline -- that's OK,
    ## the game shows a graceful error message instead of crashing)
    pause 5.0

    ## Go back to messages
    click "Back"
    pause 1.0


## ===================================================================
## RESET CHAT - Test the Clear button that resets conversation
## ===================================================================

testcase reset_chat:
    click "Start"
    pause 1.0

    ## Open Mallory's chat
    click "Mallory"
    pause 1.0

    ## Click the Clear button to reset conversation history
    click "Clear"
    pause 1.0

    ## Should still be in chat view after reset -- go back
    click "Back"
    pause 1.0
