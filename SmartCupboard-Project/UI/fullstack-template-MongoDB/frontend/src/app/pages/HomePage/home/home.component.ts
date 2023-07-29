import { Component, OnInit, ChangeDetectorRef, AfterViewInit } from '@angular/core';
import { SocketsService } from 'src/app/global/services';
import { GetData } from 'src/app/global/services/getData/getData';
import { HttpClient, HttpParams } from '@angular/common/http';
import { GlobalConstants } from 'src/app/global/mariosGlobal/mariosGlobal'
import { ThrowStmt } from '@angular/compiler';


@Component({
  selector: 'ami-fullstack-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})


export class HomeComponent implements OnInit {

  responseReceived = false;
  dataHome: any; // here you can hard-coded enter json product data (immediately in frontend angular)
  dataToPassToMiddleChild: any;
  dataToBottomBar: any;
  BottomShelfSubData = []; // initialiaze
  UpShelfSubData = []; // initialiaze
  QuantitySubData = []; // initialiaze
  ExpiringSubData = []; // initialiaze
  pageToPass = 1; // initialize to 1 ---page to pass to middle from home 

  printClickEvent(buttonEvent: number) {
    console.log('button pressed was ...  ', buttonEvent); // debug

    this.extractSubData();     // extract subData

    if (buttonEvent === 0) { // All 
      this.dataToPassToMiddleChild = this.dataHome;
    }
    else if (buttonEvent === 1) { // Top Shelf
      this.dataToPassToMiddleChild = this.UpShelfSubData;
    }
    else if (buttonEvent === 2) { // Down Shelf
      this.dataToPassToMiddleChild = this.BottomShelfSubData;
    }
    else if (buttonEvent === 3) { // Expiring
      this.dataToPassToMiddleChild = this.ExpiringSubData;
    }

    else if (buttonEvent === 4) { // Low Qty
      this.dataToPassToMiddleChild = this.QuantitySubData;
    }
    else {
      console.log('something went wrong ...');
    }

    console.log('Data to pass to middle is :'); // debug
    console.log(this.dataToPassToMiddleChild); // debug


    this.BottomShelfSubData = []; //reset
    this.UpShelfSubData = []; //reset
    this.QuantitySubData = []; //reset
    this.ExpiringSubData = []; //reset
    
    if (this.dataToPassToMiddleChild.length == 0) { // empty array
      this.dataToBottomBar = 1 ; 
    }
    else {
      if (Object.keys(this.dataToPassToMiddleChild).length % 6 == 0) {
        this.dataToBottomBar = Math.floor((Object.keys(this.dataToPassToMiddleChild).length) / 6);
      }
      else {
        this.dataToBottomBar = Math.floor((Object.keys(this.dataToPassToMiddleChild).length) / 6) + 1;
      }
    }


    console.log('dataToBottomBar is ...', this.dataToBottomBar); // debug
  }

  // extract subData
  public extractSubData() {
    this.dataHome.forEach(elementOut => {
      if (elementOut['vertical_order'] === 1) { // Up Shelf
        this.UpShelfSubData.push(elementOut);
      }
      if (elementOut['vertical_order'] === 2) { // Bottom Shelf
        this.BottomShelfSubData.push(elementOut);
      }
      if (elementOut['daysToExpire'] < this.globalConst.expiringThreshold) { // Expiring
        this.ExpiringSubData.push(elementOut);
      }
      if (elementOut['quantity'] < this.globalConst.lowQuantityPercentageThreshold * elementOut['original_weight']) { // Low Quantity
        this.QuantitySubData.push(elementOut);
      }
    });
  }

  public handleButtonTopBarEvents(buttonBottomEvent: any) {
    this.pageToPass = buttonBottomEvent;  }


  // getDataService is an instance of the class GetData , so getDataService has a method getData() to call
  constructor(public getDataService: GetData, private cdr: ChangeDetectorRef, private socketService: SocketsService, private http: HttpClient, private globalConst: GlobalConstants) { 
  }

  ngOnInit() {

    let params = new HttpParams().set('cupboardId', this.globalConst.cupboardId)

    
    let InventoryManagerIP = this.globalConst.mariosPC_IP; 
    this.http.get<any>('http://' + InventoryManagerIP + ':5002/get/Cupboard/AllProducts', { params }).subscribe(data => {
      this.dataHome = data;
      this.dataToPassToMiddleChild = this.dataHome;
      this.responseReceived = true;

      if (Object.keys(this.dataToPassToMiddleChild).length % 6 == 0) {
        this.dataToBottomBar = Math.floor((Object.keys(this.dataToPassToMiddleChild).length) / 6);
      }
      else {
        this.dataToBottomBar = Math.floor((Object.keys(this.dataToPassToMiddleChild).length) / 6) + 1;
      }
    });



    this.socketService.syncMessages("allCupboardItems").subscribe(msg => {
      console.log(msg);
      console.log('msg received from socket');
      this.dataHome = msg["message"];
      
      console.log(this.dataHome); // debug
      this.dataToPassToMiddleChild = this.dataHome;
    })

  } // end of ngOnInit()

  ngAfterViewInit() { // fix error --> ExpressionChangedAfterItHasBeenCheckedError Expression has changed after it was checked.
    this.cdr.detectChanges();
  }

}
