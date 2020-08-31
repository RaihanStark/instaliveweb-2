let is_live_now;
let currentComments = [];
let is_muted;
$(document).ready(function () {
  // clipboard
  var clipboard = new ClipboardJS(".btn");
  clipboard.on("success", function (e) {
    alert("Copied to clipboard");
  });

  // live now status
  if ($("#live_status").text() === "active") {
    is_live_now = true;
  } else {
    is_live_now = false;
  }

  if (is_live_now === true) {
    pool_viewers();
    pool_comments();
  }

  $(".startBroadcast").on("click", function () {
    $.ajax({
      type: "get",
      url: "/start_broadcast",
      beforeSend: function (xhr) {
        showLoading();
      },
      success: function (response) {
        $("#status_live").text("Running");
        $("#msg_live").val(response.message);
        hideLoading();

        $("#stopBroadcast").prop("disabled", false);
        $("#startBroadcast").prop("disabled", true);
        is_live_now = true;

        Swal.fire(
          "You're Live!",
          "Live Streaming is Starting...!",
          "success"
        ).then(function () {
          window.location = "/";
        });
        pool_viewers();
      },
      error: function (response) {
        showPopupExpiredKeyError();
        hideLoading();
      },
    });
  });

  $("#stopBroadcast").on("click", function () {
    $.ajax({
      type: "get",
      url: "/stop_broadcast",
      beforeSend: function (xhr) {
        showLoading();
      },
      success: function (response) {
        $("#status_live").text("Stopped");
        $("#msg_live").val(response.message);
        hideLoading();

        $("#stopBroadcast").prop("disabled", true);
        $("#startBroadcast").prop("disabled", false);

        is_live_now = false;

        Swal.fire(
          "You're Off!",
          "Live Streaming is Stopping...!",
          "success"
        ).then(function () {
          window.location = "/";
        });
      },
      error: function (response) {
        showPopupExpiredKeyError();
        hideLoading();
      },
    });
  });

  $("#sendMessage").on("click", function () {
    let message = $("#text_message").val();
    if (message.length >= 1) {
      $(this).attr("disabled", true);
      $.ajax({
        type: "GET",
        url: "/v1/live/comments/" + message,
        success: function (response) {
          $("#text_message").val("");
          $("#sendMessage").attr("disabled", false);
        },
      });
    }
  });

  $(".toggleMute").on("click", function () {
    // Convert data-muted string to javascript boolean
    is_muted = $(".mute-comments").attr("data-muted") == "true";

    $(".toggleMute").prop("disabled", true);

    // Sending Mute function Ajax
    $.ajax({
      type: "POST",
      url: "v1/live/mute",
      contentType: "application/json",
      data: JSON.stringify({
        muted: is_muted,
      }),
      dataType: "json",
      success: function (response) {
        $(".mute-comments").attr("data-muted", !is_muted);
        $(".toggleMute").prop("disabled", false);

        window.location = "/";
      },
    });
  });
});

function showPopupExpiredKeyError() {
  Swal.fire(
    "Streamkey is already used",
    "Restart the server to create a new stream key",
    "error"
  );
}

function showLoading() {
  $(".preloader").show();
}

function hideLoading() {
  $(".preloader").fadeOut();
}

function pool_viewers() {
  $.ajax({
    type: "GET",
    url: "/v1/live/viewers",
    dataType: "json",
    success: function (response) {
      $("#viewers_count").text(response.count);
    },
    complete: function () {
      if (is_live_now) {
        setTimeout(pool_viewers, 10000);
      }
    },
  });
}

function pool_comments() {
  $.ajax({
    type: "GET",
    url: "/v1/live/comments",
    dataType: "json",
    success: function (response) {
      if (response.comments) {
        const new_comments = response.comments;

        // If new recent comments
        new_comments.forEach((e) => {
          if (currentComments.length >= 1) {
            // Check duplicate
            let isDuplicated = currentComments.some((currentComment) => {
              return currentComment.pk == e.pk;
            });
            if (isDuplicated === false) {
              currentComments.push(e);
              appendCommentsToChat(e);

              scrollToBottomChat();
            }
          } else {
            // Append to variable
            $(".chat-list").empty();
            currentComments.push(e);
            appendCommentsToChat(e);
          }
        });
      }
    },
    complete: function () {
      if (is_live_now && !is_muted) {
        setTimeout(pool_comments, 1000);
      }
    },
  });
}

function scrollToBottomChat() {
  $(".chat-list").scrollTop($(".chat-list")[0].scrollHeight);
}

function getScrollPositionInteger() {
  return parseInt($(".chat-list").scrollTop());
}

function appendCommentsToChat(e) {
  return $(".chat-list").append(
    `
      <li>
        <div class="chat-content ">
          <h5>${e.user.username}</h5>
          <div class="box bg-light-info">${e.text}</div>
        </div>
      </li>`
  );
}
