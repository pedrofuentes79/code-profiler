use profiler_server::{add};

#[test]
fn test_add(){
    assert_eq!(add(2,3), 5);
}