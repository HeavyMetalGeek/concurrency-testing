pub fn max_deviation(value: f64, others: &[f64]) -> f64 {
    let mut max = std::f64::MIN;
    for other_value in others {
        let diff = (value - other_value).abs();
        if diff > max {
            max = diff;
        }
    }
    return max;
}
