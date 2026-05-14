package capitalgains

import "fmt"

const taxRate = 0.2

func CalculateTaxesFor(trades []Trade) ([]Tax, error) {
	totalLoss := 0.0
	weightedAveragePrice := 0.0
	currentStockQuantity := 0

	var taxes []Tax

	for _, t := range trades {
		if !t.Operation.Valid() {
			return nil, fmt.Errorf("invalid operation: %s", t.Operation)
		}

		if t.Operation == Buy {
			weightedAveragePrice = ((float64(currentStockQuantity) * weightedAveragePrice) + (float64(t.Quantity) * t.UnitCost)) / float64(currentStockQuantity + t.Quantity)
			currentStockQuantity += t.Quantity
			taxes = append(taxes, Tax{Tax: 0})
		}

		if t.Operation == Sell {
			tradeAmount := t.UnitCost * float64(t.Quantity)
			costOfPurchase := weightedAveragePrice * float64(t.Quantity)
			profitInTransaction := tradeAmount - costOfPurchase

			taxableProfit := 0.0

			if profitInTransaction < 0 {
				// realized loss → accumulate
				totalLoss += -profitInTransaction
			} else if tradeAmount > 20_000 {
				// realized profit → consume past losses
				if totalLoss > 0 {
					if profitInTransaction <= totalLoss {
						totalLoss -= profitInTransaction
						taxableProfit = 0
					} else {
						taxableProfit = profitInTransaction - totalLoss
						totalLoss = 0
					}
				} else {
					taxableProfit = profitInTransaction
				}
			}

			
			if taxableProfit > 0 {
				taxes = append(taxes, Tax{Tax: float32(taxableProfit) * float32(taxRate)})
			} else {
				taxes = append(taxes, Tax{Tax: 0})
			}

			currentStockQuantity -= t.Quantity
		}

    }

	return taxes, nil
}