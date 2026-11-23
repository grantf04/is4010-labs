// Week 13: Idiomatic Rust
//
// Practice three pillars of idiomatic Rust:
//   Part 1: iterators and closures
//   Part 2: error handling with Result
//   Part 3: smart pointers (Box for recursive types)
//
// Run: cargo test

use std::fmt;

fn main() {
    println!("Week 13: Idiomatic Rust");
}

// ============================================================================
// PART 1: Iterators and closures
// ============================================================================

/// Analyses a string of text and returns a tuple:
///   (word_count, average_word_length, longest_word)
///
/// - Words are separated by whitespace.
/// - `average_word_length` is 0.0 for empty input.
/// - `longest_word` is an empty String for empty input.
///
/// Hint: use iterator adaptors (.split_whitespace(), .map(), .max_by_key(), etc.)
pub fn analyze_text(text: &str) -> (usize, f64, String) {
    let (count, total_length, longest, _) = text
        .split_whitespace()
        .map(|word| (word, word.chars().count()))
        .fold(
            (0, 0, "", 0),
            |(count, total, longest, longest_length), (word, length)| {
                let (longest, longest_length) = if length > longest_length {
                    (word, length)
                } else {
                    (longest, longest_length)
                };
                (count + 1, total + length, longest, longest_length)
            },
        );
    let average = if count == 0 {
        0.0
    } else {
        total_length as f64 / count as f64
    };
    (count, average, longest.to_owned())
}

/// Returns the sum of the squares of all even numbers in `numbers`.
///
/// Example: [1, 2, 3, 4] → 2² + 4² = 4 + 16 = 20
///
/// Hint: .filter(), .map(), .sum()
pub fn process_numbers(numbers: &[i32]) -> i32 {
    numbers
        .iter()
        .filter(|&&number| number % 2 == 0)
        .map(|&number| number * number)
        .sum()
}

/// Returns a closure that counts up from 1 each time it is called.
///
/// ```
/// let mut counter = make_counter();
/// assert_eq!(counter(), 1);
/// assert_eq!(counter(), 2);
/// assert_eq!(counter(), 3);
/// ```
pub fn make_counter() -> impl FnMut() -> i32 {
    let mut count = 0;
    move || {
        count += 1;
        count
    }
}

// ============================================================================
// PART 2: Error handling with Result
// ============================================================================

/// Divides `a` by `b`.
/// Returns `Ok(result)` on success, or `Err("division by zero")` when `b` is 0.0.
pub fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("division by zero".to_owned())
    } else {
        Ok(a / b)
    }
}

/// Error type for parse_positive_number.
#[derive(Debug, PartialEq)]
pub enum ParseError {
    /// The input string could not be parsed as an integer.
    NotANumber,
    /// The parsed number is zero or negative.
    NotPositive,
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(match self {
            Self::NotANumber => "input is not a valid integer",
            Self::NotPositive => "number must be positive",
        })
    }
}

/// Parses `input` as a positive integer (> 0).
/// Returns the number on success, or an appropriate `ParseError` on failure.
pub fn parse_positive_number(input: &str) -> Result<i32, ParseError> {
    let number = input.parse::<i32>().map_err(|_| ParseError::NotANumber)?;
    if number > 0 {
        Ok(number)
    } else {
        Err(ParseError::NotPositive)
    }
}

// ============================================================================
// TESTS: DO NOT MODIFY
// ============================================================================
#[cfg(test)]
mod tests {
    use super::*;

    // --- analyze_text ---

    #[test]
    fn test_analyze_text_basic() {
        let (count, avg, longest) = analyze_text("hello world rust");
        assert_eq!(count, 3);
        // avg = (5 + 5 + 4) / 3 = 14/3 ≈ 4.666…
        assert!((avg - 14.0 / 3.0).abs() < 1e-9);
        assert_eq!(longest, "hello"); // or "world", both length 5; either accepted
    }

    #[test]
    fn test_analyze_text_empty() {
        let (count, avg, longest) = analyze_text("");
        assert_eq!(count, 0);
        assert_eq!(avg, 0.0);
        assert_eq!(longest, "");
    }

    #[test]
    fn test_analyze_text_single_word() {
        let (count, avg, longest) = analyze_text("Rust");
        assert_eq!(count, 1);
        assert_eq!(avg, 4.0);
        assert_eq!(longest, "Rust");
    }

    // --- process_numbers ---

    #[test]
    fn test_process_numbers_mixed() {
        // evens: 2, 4 → 4 + 16 = 20
        assert_eq!(process_numbers(&[1, 2, 3, 4]), 20);
    }

    #[test]
    fn test_process_numbers_all_odd() {
        assert_eq!(process_numbers(&[1, 3, 5]), 0);
    }

    #[test]
    fn test_process_numbers_empty() {
        assert_eq!(process_numbers(&[]), 0);
    }

    #[test]
    fn test_process_numbers_negative_evens() {
        // -2² = 4, 4² = 16 → 20
        assert_eq!(process_numbers(&[-2, -1, 4]), 20);
    }

    // --- make_counter ---

    #[test]
    fn test_make_counter_increments() {
        let mut counter = make_counter();
        assert_eq!(counter(), 1);
        assert_eq!(counter(), 2);
        assert_eq!(counter(), 3);
    }

    #[test]
    fn test_make_counter_independent() {
        let mut c1 = make_counter();
        let mut c2 = make_counter();
        assert_eq!(c1(), 1);
        assert_eq!(c1(), 2);
        assert_eq!(c2(), 1); // c2 is independent of c1
    }

    // --- divide ---

    #[test]
    fn test_divide_ok() {
        assert_eq!(divide(10.0, 2.0), Ok(5.0));
    }

    #[test]
    fn test_divide_by_zero() {
        assert!(divide(5.0, 0.0).is_err());
    }

    #[test]
    fn test_divide_negative() {
        assert_eq!(divide(-9.0, 3.0), Ok(-3.0));
    }

    // --- parse_positive_number ---

    #[test]
    fn test_parse_positive_number_ok() {
        assert_eq!(parse_positive_number("42"), Ok(42));
        assert_eq!(parse_positive_number("1"), Ok(1));
    }

    #[test]
    fn test_parse_positive_number_not_a_number() {
        assert_eq!(parse_positive_number("abc"), Err(ParseError::NotANumber));
        assert_eq!(parse_positive_number(""), Err(ParseError::NotANumber));
    }

    #[test]
    fn test_parse_positive_number_not_positive() {
        assert_eq!(parse_positive_number("0"), Err(ParseError::NotPositive));
        assert_eq!(parse_positive_number("-5"), Err(ParseError::NotPositive));
    }

    #[test]
    fn test_parse_error_display() {
        // Just verify Display doesn't panic and returns something.
        let msg = format!("{}", ParseError::NotANumber);
        assert!(!msg.is_empty());
        let msg2 = format!("{}", ParseError::NotPositive);
        assert!(!msg2.is_empty());
    }
}
