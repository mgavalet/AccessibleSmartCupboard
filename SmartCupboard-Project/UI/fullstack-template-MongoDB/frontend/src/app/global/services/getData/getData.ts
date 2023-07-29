import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";

@Injectable({
    providedIn: 'root'
})

export class GetData {

    private hostURI : string ; 
    
    constructor (private http: HttpClient){
        this.hostURI = environment.host;
    }
}

// Here is the implementation of a SERVICE named getData
// use that service in every component you want