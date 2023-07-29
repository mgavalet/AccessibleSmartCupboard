import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'ami-fullstack-moderator-page',
  templateUrl: './moderator-page.component.html',
  styleUrls: ['./moderator-page.component.scss']
})
export class ModeratorPageComponent implements OnInit {

  pageNum: any;
  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.pageNum = 0; // initialize pageNum to 0
    console.log('pageNum is now: ', this.pageNum);
  }


  // create a public function named goToPreviousPage that will decrease the pageNum by 1 and console.log the new pageNum
  public goToPreviousPage() {
    if (this.pageNum > 0) {
      this.pageNum--;
      console.log('pageNum is now: ', this.pageNum);

      var body = { "pageNum": this.pageNum };
      this.http.post<any>('http://localhost:8080/api/getData/broadcast/changeAmiPage', body).subscribe(data => { // CAUTION ! IP could be changed 
        console.log('Received data is : ', data);
      });

    }
  }

  public goToNextPage() {
    if (this.pageNum < 10) {
      this.pageNum++;
      console.log('pageNum is now: ', this.pageNum);

      var body = { "pageNum": this.pageNum };
      this.http.post<any>('http://localhost:8080/api/getData/broadcast/changeAmiPage', body).subscribe(data => { // CAUTION ! IP could be changed 
        console.log('Received data is : ', data);
      });
    }
  }

  public delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // lights
  public lightCup2() {
    (async () => {

      for (let i = 0; i < 5; i++) {
        // Do something before delay
        this.redColor();

        await this.delay(800);

        // Do something after
        this.switchoff();
        await this.delay(800);

      }
    })();

  }

  public redColor() {
    var body = {
      "cupId": 2,
      "color": "red"
    };

    this.http.post<any>('http://localhost:8080/api/getData/broadcast/lightVirtualCupsDoors', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public lightCup3() {
    (async () => {

      for (let i = 0; i < 5; i++) {
        // Do something before delay
        this.greenColor();

        await this.delay(800);

        // Do something after
        this.switchoff();
        await this.delay(800);
      }
    })();
  }

  public greenColor() {
    var body = {
      "cupId": 3,
      "color": "green"
    };

    this.http.post<any>('http://localhost:8080/api/getData/broadcast/lightVirtualCupsDoors', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public switchoff() {
    var body = {
      "cupId": 3798,
      "color": "transparent"
    };

    this.http.post<any>('http://localhost:8080/api/getData/broadcast/lightVirtualCupsDoors', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }
  public lightEmptySLotsCup3() {
    (async () => {

      for (let i = 0; i < 5; i++) {
        // Do something before delay
        this.yellowColor();

        await this.delay(800);

        // Do something after
        this.switchoff();
        await this.delay(800);
      }
    })();
  }

  
  public yellowColor() {
    var body = {
      "cupId": 3,
      "color": "yellow"
    };

    this.http.post<any>('http://localhost:8080/api/getData/broadcast/lightVirtualCupsDoors', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  // light Real Cupboard
  public ExpiringMushroom() {
    var body1 = {
      'ledstripeId': 1, // inside Cupboard is lestripe = 1 
      'startLed': 46,
      'endLed': 56,
      'color': 'red'
    };

    this.http.post<any>('http://139.91.96.156/lights/ConstantFromToLedIDs', body1).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });


    // blink red light at the door of cupboard 1
    var body2 = {
      "startLed": "1",
      "endLed": "22",
      "color": "red",
      "blinkingDuration": "800",
      "totalEventDuration": "8000",
      "ledstripeId": "0"
    };

    this.http.post<any>('http://139.91.96.156/lights/blinkSomeLeds', body2).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public EmptySlots() {
    var body1 = {
      'ledstripeId': 1, // inside Cupboard is lestripe = 1 
      'startLed': 23,
      'endLed': 35,
      'color': 'yellow'
    };

    this.http.post<any>('http://139.91.96.156/lights/ConstantFromToLedIDs', body1).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

  }

  public EmptySlots2() {
    var body2 = {
      'ledstripeId': 1, // inside Cupboard is lestripe = 1 
      'startLed': 97,
      'endLed': 112,
      'color': 'yellow'
    };

    this.http.post<any>('http://139.91.96.156/lights/ConstantFromToLedIDs', body2).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public RiceGreenLight() {

    var body2 = {
      'color': 'green'
    };

    this.http.post<any>('http://139.91.96.156/lights/ConstantDoor', body2).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

    var body1 = {
      'ledstripeId': 1, // inside Cupboard is lestripe = 1 
      'startLed': 67,
      'endLed': 77,
      'color': 'green'
    };

    this.http.post<any>('http://139.91.96.156/lights/ConstantFromToLedIDs', body1).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public CloseCup1() {
    // close Cupboard 1
    this.http.post<any>('http://139.91.96.156/door/close', {}).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

    // switch off lights inside
    this.http.post<any>('http://139.91.96.156/lights/switchoff', { "ledstripeId": 1 }).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public OpenCup1() {
    // open Cupboard 1
    this.http.post<any>('http://139.91.96.156/door/open', {}).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

    // switch off lights outside
    this.http.post<any>('http://139.91.96.156/lights/switchoff', { "ledstripeId": 0 }).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  // audio
  public startCooking() {
    var body = {
      "audioFileName": "StartCooking.mp3",
      "customMode": "no",
      "textToSpeech": "Why "
    };

    this.http.post<any>('http://localhost:5001/playAudio', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public wrongMushroom() {
    var body = {
      "audioFileName": "WrongMushroom.mp3",
      "customMode": "no",
      "textToSpeech": "Why "
    };

    this.http.post<any>('http://localhost:5001/playAudio', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public startStoring() {
    var body = {
      "audioFileName": "StartManagingItems.mp3",
      "customMode": "no",
      "textToSpeech": "Why "
    };

    this.http.post<any>('http://localhost:5001/playAudio', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public tsigarisma() {
    var body = {
      "audioFileName": "tsigarisma.mp3",
      "customMode": "no",
      "textToSpeech": "Why "
    };

    this.http.post<any>('http://localhost:5001/playAudio', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public emptySlots() {
    var body = {
      "audioFileName": "emptySlots.mp3",
      "customMode": "no",
      "textToSpeech": "Why "
    };

    this.http.post<any>('http://localhost:5001/playAudio', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public expiringProducts() {
    var body = {
      "audioFileName": "expiringProducts.mp3",
      "customMode": "no",
      "textToSpeech": "Why "
    };

    this.http.post<any>('http://localhost:5001/playAudio', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public sugarLocation() {
    var body = {
      "audioFileName": "sugarLocation.mp3",
      "customMode": "no",
      "textToSpeech": "Why "
    };

    this.http.post<any>('http://localhost:5001/playAudio', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });
  }

  public Reset() {
    // switch off lights inside
    this.http.post<any>('http://139.91.96.156/lights/switchoff', { "ledstripeId": 1 }).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

    // switch off lights outside
    this.http.post<any>('http://139.91.96.156/lights/switchoff', { "ledstripeId": 0 }).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

    // Switch off lights of virtual cupboards 
    var body = {
      "cupId": 3798,
      "color": "transparent"
    };

    this.http.post<any>('http://localhost:8080/api/getData/broadcast/lightVirtualCupsDoors', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

    // make door homing via HTTP request
    this.http.post<any>('http://139.91.96.156/door/homing', {}).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });

    // go to first image in AMI page
    this.pageNum = 0;
    var body2 = { "pageNum": this.pageNum };
    this.http.post<any>('http://localhost:8080/api/getData/broadcast/changeAmiPage', body2).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ', data);
    });


  }

}

