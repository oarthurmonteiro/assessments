package main

import (
	"bufio"
	"capital-gains-cli/internal/capitalgains"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

func processBatch(inputs []string) {

	for _, i := range inputs {

		i = strings.TrimSpace(i)
		if i == "" {
			return
		}

		var trades []capitalgains.Trade
		if err := json.Unmarshal([]byte(i), &trades); err != nil {
			fmt.Println("invalid JSON:", err)
			return
    	}

		taxes, err := capitalgains.CalculateTaxesFor(trades)
		if err != nil {
			fmt.Println(err)
			return
		}

		b, _ := json.Marshal(taxes)
		fmt.Println(string(b))
	}
}

func main() {
    scanner := bufio.NewScanner(os.Stdin)
    var buffer []string

    fmt.Println("Enter JSON. Blank line to process:")

    for scanner.Scan() {
        line := scanner.Text()

        // Blank line → process current buffer
        if strings.TrimSpace(line) == "" {
            processBatch(buffer)
            buffer = buffer[:0] // reset buffer
            continue
        }

        buffer = append(buffer, line)
    }

    // Process remaining input on EOF
    if len(buffer) > 0 {
		processBatch(buffer)
    }

    if err := scanner.Err(); err != nil {
        panic(err)
    }
}
