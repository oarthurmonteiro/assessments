namespace AutomatedInvestment.Domain.Common;

public class Result
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    
    // Agora temos uma coleção de erros
    private readonly List<string> _errors = [];
    public IReadOnlyCollection<string> Errors => _errors.AsReadOnly();

    protected Result(bool isSuccess, IEnumerable<string>? errors = null)
    {
        IsSuccess = isSuccess;
        if (errors != null) _errors.AddRange(errors);
    }

    public static Result Success() => new(true);
    public static Result Failure(string error) => new(false, [error]);
    public static Result Failure(IEnumerable<string> errors) => new(false, errors);
}

public class Result<T> : Result
{
    private readonly T? _value;

    public T Value => IsSuccess 
        ? _value! 
        : throw new InvalidOperationException($"Impossível acessar o valor. Erros: {string.Join(", ", Errors)}");

    protected Result(T? value, bool isSuccess, IEnumerable<string>? errors = null) 
        : base(isSuccess, errors)
    {
        _value = value;
    }

    public static Result<T> Success(T value) => new(value, true);
    public static new Result<T> Failure(string error) => new(default, false, [error]);
    public static new Result<T> Failure(IEnumerable<string> errors) => new(default, false, errors);

    public static implicit operator Result<T>(T value) => Success(value);
}