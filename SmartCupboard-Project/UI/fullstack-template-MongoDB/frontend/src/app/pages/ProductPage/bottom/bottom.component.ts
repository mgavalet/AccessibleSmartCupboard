import { Component, OnInit,Input,Output,EventEmitter} from '@angular/core';

@Component({
  selector: 'ami-fullstack-bottom',
  templateUrl: './bottom.component.html',
  styleUrls: ['./bottom.component.scss']
})
export class BottomComponent implements OnInit {


  currentNumPage : number = 1 ; // initialize

  public sendInfoEvent(value: any) {
    this.newPressedPageEvent.emit(value); // send info to parent component
  }

  @Input () totalPages ; 
  @Output() newPressedPageEvent = new EventEmitter<any>();

  constructor() { }

  ngOnInit() {
    this.sendInfoEvent(this.currentNumPage) ;   // send to home component parent the current page info
  
  }

  goToPreviousPage(pageNum:number){
   
    if (pageNum > 1 && pageNum <= this.totalPages){
      this.currentNumPage --;
      
    }

    else{
      this.currentNumPage = 1 ;
    }
      this.sendInfoEvent(this.currentNumPage) ;   // send to home component parent the current page info

  }
  
  goToNextPage(pageNum:number){
    if (pageNum >= 1 && pageNum < this.totalPages){
      this.currentNumPage ++;
    }
    
    else{
      this.currentNumPage = this.totalPages ;
    }   
      this.sendInfoEvent(this.currentNumPage) ; // send to home component parent the current page info  

  }
}
