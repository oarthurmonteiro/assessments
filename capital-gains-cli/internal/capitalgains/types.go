package capitalgains

type Operation string

const (
    Buy  Operation = "buy"
    Sell Operation = "sell"
)

func (o Operation) Valid() bool {
    return o == Buy || o == Sell
}

type Trade struct {
    Operation Operation `json:"operation"`
    UnitCost  float64   `json:"unit-cost"`
    Quantity  int       `json:"quantity"`
}

type Tax struct {
    Tax float32 `json:"tax"`
}