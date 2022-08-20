package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/spf13/viper"
)

// import "fmt"
type APIRequest struct {
	Model             string  `json:"model"`
	Prompt            string  `json:"prompt"`
	Temperature       float32 `json:"temperature"`
	Max_tokens        int     `json:"max_tokens"`
	Top_p             float32 `json:"top_p"`
	Frequency_penalty float32 `json:"frequency_penalty"`
	Presence_penalty  float32 `json:"presence_penalty"`
}
type APIResponse struct {
	ID      string `json:"id"`
	Object  string `json:"object"`
	Created int    `json:"created"`
	Model   string `json:"model"`
	Choices []struct {
		Text         string      `json:"text"`
		Index        int         `json:"index"`
		Logprobs     interface{} `json:"logprobs"`
		FinishReason string      `json:"finish_reason"`
	} `json:"choices"`
	Usage struct {
		PromptTokens     int `json:"prompt_tokens"`
		CompletionTokens int `json:"completion_tokens"`
		TotalTokens      int `json:"total_tokens"`
	} `json:"usage"`
}

func main() {
	response := GetTopics("Computer Science")
	j, err := json.Marshal(response)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
	} else {
		fmt.Println(string(j))
	}
	println(response[0])
}

func GetTopics(subject string) []string {
	var newAPIRequest = APIRequest{Model: "text-curie-001", Prompt: `List of every topic related to "` + subject + `":\n`, Temperature: 0, Max_tokens: 256, Top_p: 1, Frequency_penalty: 0, Presence_penalty: 0}
	response := API(newAPIRequest)

	text := []byte(response)
	var p APIResponse
	err := json.Unmarshal(text, &p)
	if err != nil {
		panic(err)
	}
	topics := (strings.Replace(p.Choices[0].Text, "\n", "", -1))
	return strings.Split(topics, "-")[1:]
}

func API(request APIRequest) string {
	viper.SetConfigFile(".env")
	viper.ReadInConfig()
	j, err := json.Marshal(request)
	if err != nil {
		log.Fatal(err)
	}
	body := strings.NewReader(string(j))
	req, err := http.NewRequest("POST", "https://api.openai.com/v1/completions", body)
	if err != nil {
		log.Fatal(err)
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", os.ExpandEnv("Bearer "+viper.GetString("OPENAI_API_KEY")))

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	b, err := io.ReadAll(resp.Body)
	// b, err := ioutil.ReadAll(resp.Body)  Go.1.15 and earlier
	if err != nil {
		log.Fatalln(err)
	}

	return (string(b))
}
