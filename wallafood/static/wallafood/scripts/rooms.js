$(function() {
    // Reference to the chat messages area
    let $chatWindow = $("#messages");
  
    // Our interface to the Chat service
    let chatClient;
  
    // A handle to the room's chat channel
    let roomChannel;
  
    // The server will assign the client a random username - stored here
    let username;
  
    // Helper function to print info messages to the chat window
    function print(infoMessage, asHtml) {
      let $msg = $('<div class="info">');
      if (asHtml) {
        $msg.html(infoMessage);
      } else {
        $msg.text(infoMessage);
      }
      $chatWindow.append($msg);
    }
  
    // Helper function to print chat message to the chat window
    function printMessage(fromUser, message) {
      if (fromUser === username) {
        let $cont1 = $('<div class="outgoing_msg">');
        let $from = $('<span>').text("User: " + fromUser);
        let $cont2 = $('<div class="sent_msg">');
        let $txt = $('<p>').text(message);
        $cont2.append($from);
        $cont2.append($txt);
        $cont1.append($cont2);
        $chatWindow.append($cont1);
        $chatWindow.scrollTop($chatWindow[0].scrollHeight);
      } else {
        let $cont1 = $('<div class="incoming_msg">');
        let $from = $('<span>').text("User: " + fromUser);
        let $cont2 = $('<div class="received_msg">');
        let $cont3 = $('<div class="received_withd_msg">');
        let $txt = $('<p>').text(message);
        $cont3.append($from);
        $cont3.append($txt);
        $cont2.append($cont3);
        $cont1.append($cont2);
        $chatWindow.append($cont1);
        $chatWindow.scrollTop($chatWindow[0].scrollHeight);
      }
    }
  
    // Get an access token for the current user, passing a device ID
    // for browser-based apps, we'll just use the value "browser"
    $.getJSON(
      "/wallafood/token",
      {
        device: "browser"
      },
      function(data) {
        // Alert the user they have been assigned a random username
        username = data.identity;
  
        // Initialize the Chat client
        // chatClient = new Twilio.Chat.Client(data.token);
  
        Twilio.Chat.Client.create(data.token).then(client => {
          // Use client
          chatClient = client;
          chatClient.getSubscribedChannels().then(createOrJoinChannel);
        });
      }
    );
  
    // Set up channel after it has been found / created
    function setupChannel(name) {

      if(roomChannel.state.status !== "joined") {

        roomChannel.join();
      }

      print(
        `Joined channel ${name} as <span class="me"> ${username} </span>.`,
        true
      );

      // Listen for new messages sent to the channel
      roomChannel.on("messageAdded", function(message) {
        printMessage(message.author, message.body);
      });
    }
  
    function processPage(page) {
      page.items.forEach(message => {
        printMessage(message.author, message.body);
      });
      if (page.hasNextPage) {
        page.nextPage().then(processPage);
      } else {
        console.log("Done loading messages");
      }
    }
  
    function createOrJoinChannel(channels) {
      // Extract the room's channel name from the page URL
      let channelName = window.location.pathname.split("/").slice(-2, -1)[0];
    
      chatClient
        .getChannelByUniqueName(channelName)
        .then(function(channel) {
          roomChannel = channel;
          console.log("Found channel:", channelName);
          setupChannel(channelName);
        })
        .catch(function() {
          // If it doesn't exist, let's create it
          chatClient
            .createChannel({
              uniqueName: channelName,
              friendlyName: `${channelName} Chat Channel`
            })
            .then(function(channel) {
              roomChannel = channel;
              setupChannel(channelName);
            });
        });
    }
  
    // Add newly sent messages to the channel
    let $form = $("#write-form");
    let $input = $("#message-input");
    $form.on("submit", function(e) {
      e.preventDefault();
      if (roomChannel && $input.val().trim().length > 0) {
        roomChannel.sendMessage($input.val());
        $input.val("");
      }
    });
  });