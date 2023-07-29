import { Component, OnInit } from '@angular/core';
import { GetData } from 'src/app/global/services/getData/getData'; 
import { SocketsService } from 'src/app/global/services';
import { HttpClient, HttpParams } from '@angular/common/http';
import { GlobalConstants } from 'src/app/global/mariosGlobal/mariosGlobal'
import {Router} from '@angular/router'

@Component({
  selector: 'ami-fullstack-product-page',
  templateUrl: './product-page.component.html',
  styleUrls: ['./product-page.component.scss']
})
export class ProductPageComponent implements OnInit {

  PageTitleName: any; // The product name which is the title of the page 

  numberOfItems: any; // to show to right corner -- top bar
  totalQuantity: any; // to show to right corner -- top bar

  dataToBottomBar: any;
  responseReceived = false;

  dataToPassToMiddleChild: any;
  currentPageInBottom: any;
  startIdx: any;
  endIdx: any;

  constructor(public getDataService: GetData,private router:Router, private socketService: SocketsService, private http: HttpClient, private globalConst: GlobalConstants) { }

  public onRightClick() { // disable right click 
    return false;
  }


  public getBottomDataToPass() {
    if (Object.keys(this.dataToPassToMiddleChild).length % 3 == 0) {
      this.dataToBottomBar = Math.floor((Object.keys(this.dataToPassToMiddleChild).length) / 3);
    }
    else {
      this.dataToBottomBar = Math.floor((Object.keys(this.dataToPassToMiddleChild).length) / 3) + 1;
    }
    console.log('dataToBottomBar is ...', this.dataToBottomBar); // debug
  }

  ngOnInit() {

    console.log('Product Name passed from HomePage is ... ', history.state.data);  // debug
    this.PageTitleName = history.state.data;

    let params = new HttpParams().set('cupboardId', this.globalConst.cupboardId).set('item', this.PageTitleName);

    let InventoryManagerIP = this.globalConst.mariosPC_IP; 

    this.http.get<any>('http://' + InventoryManagerIP + ':5002/get/info/ForAnItem/InCupboard', { params }).subscribe(data => {
      console.log('Received info for item is : ', data);
      this.dataToPassToMiddleChild = data;
      console.log('Page title name is ...', this.PageTitleName); // debug  
      var returnValues = this.getCornerInfo(); // Items and Quantity 
      this.numberOfItems = returnValues[0];
      this.totalQuantity = returnValues[1];

      console.log('numberOfItems : ', this.numberOfItems, 'totalQuantity : ', this.totalQuantity); // debug 

      this.getBottomDataToPass();
      this.responseReceived = true;


      // navigate to HomePage after 120 seconds = 2 minutes
      setTimeout(() => {
        document.location.href = 'http://139.91.96.130:4200/'; // IP maybe change
      }, 120000);
    });


  } // end of ngOnInit


  public handleButtonBottomBarEvents(buttonBottomEvent: any) {


    console.log("BOTTOM PRESSED..."); // debug
  }

  public getCornerInfo() {
    // get the length of the array
    var numberOfItems = this.dataToPassToMiddleChild.length;

    var sumQuant = 0;

    this.dataToPassToMiddleChild.forEach(element => {
      sumQuant += element['quantity'];
    });

    sumQuant /= 1000; // convert gr to Kg 
    return [numberOfItems, sumQuant];
  }

}