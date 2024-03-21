<<<<<<< HEAD
package main

import "net/http"

func main() {

	http.ListenAndServe(":8080", http.FileServer(http.Dir("./html")))

}
=======
package main

import "net/http"

func main() {

	http.ListenAndServe(":8080", http.FileServer(http.Dir("./html")))

}
>>>>>>> e9b95997cfe2d1f33587106b547c72d30d5f5847
