use std::time::{Duration, Instant};
use std::sync::Arc;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    let nvalues: usize = if args.len() < 2 {
        1000
    } else {
        args[1].parse()?
    };

    let data: Vec<f64> = (0..nvalues)
        .into_iter()
        .map(|_| rand::random::<f64>())
        .collect();

    let start_time = Instant::now();
    let data_cpy = data.to_owned();
    let data_arc = Arc::new(data_cpy);
    let mut threads = Vec::new();
    let mut results = Vec::new();
    for value in data.iter() {
        let data_ptr = data_arc.clone();
        let value_cpy = value.clone();
        let handle = tokio::task::spawn_blocking(move || {
            tasks::max_deviation(value_cpy, &data_ptr);
        });
        threads.push(handle);
    }
    for thd in threads {
        results.push(thd.await?);
    }
    let stop_time = Instant::now();
    let std_time = stop_time.duration_since(start_time).as_nanos();
    println!("\narray_compare (std::thread):");
    println!("\t{} calculations", data.len());
    println!("\t{} ns", std_time);
    println!("\t{} s", std_time as f64 / 1e9);
    return Ok(());
}
