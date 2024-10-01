<template>
  <div class="my-component">
    <div>
      <h1>{{ title }}</h1>
    </div>
    <div id="chat-body">
      <div id="messages" v-if="messages != ''">
        <div v-for="[key, message] of Object.entries(messages)" :key="key" :class="key[0]">
          <div>{{ message }}</div>
        </div>
      </div>
      <div id=" messages" v-else>no message yet !</div>
      <div id="user-txt">
        <span id="loading-ico" v-if="sending" class="material-symbols-outlined">
          autorenew
        </span>
        <input type="text" placeholder="Type your text there" @keydown.enter="makeRequest" v-model="prompt">
        <button id="send-btn" @click="makeRequest">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Chatroom',
  data() {
    return {
      title: 'ChatBot',
      messages: {},
      prompt: "",
      counter: 0,
      sending: false,
      service_start_resquest: `start_message_for_the_service ~ You are Clara, the friendly and helpful virtual assistant for VenTou, a store that provides high-quality products. Your task is to assist customers in finding products, answering their questions, and guiding them through the purchase process. You should:

                                Greet each customer warmly and introduce yourself as Clara from VenTou.

                                Ask the customer how you can assist them.

                                Help the customer find products based on their needs by asking relevant questions about their preferences.

                                If the customer decides to make a purchase, politely ask for the following details:

                                Their phone number.
                                Their location  (address).
                                Any special delivery instructions (e.g., preferred delivery times or any restrictions).
                                Their preferred payment method (cash, card, mobile money, etc.).
                                The item(s) they wish to purchase and quantity.
                                An email address for sending a receipt (if applicable).
                                Make sure to respond naturally and professionally, offering personalized recommendations when needed.

                                When the customer has finished their purchase, confirm the order details, including contact information, delivery preferences, and payment.

                                Offer VenTou's store contact information (0556884867) if the customer has any further questions or issues.

                                Maintain a friendly and efficient conversation, ensuring the customer feels valued and taken care of.

                                Your goal is to assist customers with the same level of professionalism and care as a human assistant would.`,
      start: true,
    }
  },
  mounted() {
    this.prompt = this.service_start_resquest;
    this.makeRequest();
  },
  methods: {
    makeRequest() {
      this.counter++;
      if (!this.start) {
        this.messages['h' + this.counter] = this.prompt;
      }
      this.start = false;
      this.counter++;


      const data = {
        model: "llama3",
        prompt: this.prompt
      };
      this.prompt = "";
      this.sending = true;
      axios.post('http://localhost:8000', data)
        .then(response => {
          this.messages['b' + this.counter] = response.data;
          this.sending = false;
        })
        .catch(error => {
          console.error('There was an error!', error);
          this.sending = false;
        });
    }
  }
}
</script>

<style scoped>
.my-component {
  background-color: black;
  padding: 20px;
  border-radius: 5px;
  color: white;
  box-shadow: 0 30px 50px rgba(0, 0, 0, 0.3);
  text-align: center;
  font-family: Arial, sans-serif;
  height: 800px;
  width: 100%;
}

#chat-body {
  display: flex;
  flex-direction: column;
  justify-content: end;
  height: 90%;
  gap: 10px;
}

#user-txt {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: rgb(37, 37, 37);
  padding: 10px;
}

#user-txt * {
  padding: 10px;
}


#send-btn {
  background-color: rgb(0, 0, 0);
  color: white;
  border: none;
  box-shadow: 0 30px 50px rgba(0, 0, 0, 0.3);
  border-radius: 5px;
}

#messages {
  border: 1px solid gray;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: end;
  overflow-y: scroll;
}

.h {
  width: 100%;
  padding: 10px;
  margin: 10px;
  display: flex;
  justify-content: end;
  max-width: 96%;
}

.h div {
  background-color: gray;
  width: max-content;
  padding: 10px;
  margin: 10px;
}

.b {
  background-color: white;
  color: black;
  width: 100%;
  overflow-x: wrap;
  padding: 10px;
  margin: 10px;
  max-width: 90%;
}

.b div {
  background-color: white;
  color: black;
  width: 100%;
  overflow-x: wrap;
  text-align: left;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

#loading-ico {
  animation: rotate 3s linear infinite;
}
</style>