// edw grafw kati me tin morfi san to socket-events.controller.ts

import { Request, Response, NextFunction, Router } from 'express';
import { DIContainer, SocketsService } from '@app/services';
import { NO_CONTENT } from 'http-status-codes';

export class getData {

  /**  * Apply all routes for socket events
   * POST /socket-events/broadcast/:event   Broadcasts an event to all clients
   *
   * @returns {Router}
   */
  public applyRoutes(): Router {
    const router = Router();

    router.post('/data', this.broadcast())
          .post('/broadcast/test', this.test)
          .post('/broadcast/changeAmiPage', this.changeAmiPage) // new new 
          .post('/broadcast/lightVirtualCupsDoors', this.lightVirtualCupsDoors); // new new 

    return router;
  }

  /**
   * Broadcasts an event to all clients
   */
  public broadcast() {
    return async (req: Request, res: Response, next?: NextFunction): Promise<Response> => {
      try {
        console.log("get data");
        res.status(200);
        return;
      } catch (e) {
        next(e);
      }
    };
  }

  public test(req: Request, res: Response, next?: NextFunction) {
    const socketService = DIContainer.get(SocketsService);
    socketService.broadcast("allCupboardItems", req.body); // publish in the pubsub channel named "allCupboardItems"
    console.log(req.body); // debug
    res.send("NASAIKALABRO");
  }


  public changeAmiPage(req: Request, res: Response, next?: NextFunction) {
    const socketService = DIContainer.get(SocketsService);
    socketService.broadcast("amiPages", req.body); // publish in the pubsub channel named "amiPages"
    console.log(req.body); // debug
    res.send({"msg" : "NASAIKALABROO"}); // this is printed in POSTMAN - returned response
  }

  public lightVirtualCupsDoors (req: Request, res: Response, next?: NextFunction) {
    const socketService = DIContainer.get(SocketsService);
    socketService.broadcast("lightVirtualCupsDoors", req.body); // publish in the pubsub channel named "lightVirtualCupsDoors"
    console.log(req.body); // debug
    res.send({"msg" : "NASAIKALABROOO"}); // this is printed in POSTMAN - returned response
  }

} // end of getData class