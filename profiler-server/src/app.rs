use axum::{Router};

pub async fn create_app() -> Router {
    Router::new()
        .route("/hello", axum::routing::get(|| async { "Hello, World!" }))
        
        
}

