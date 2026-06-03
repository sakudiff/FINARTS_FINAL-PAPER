import "../index.d-BiUz7kM_.cjs";
import { AnyRouter } from "../unstable-core-do-not-import.d-Dh9CT5RO.cjs";
import "../index.d-CvZXeEyR.cjs";
import { NodeHTTPCreateContextFnOptions, NodeHTTPHandlerOptions } from "../index.d-fBAdSX6g.cjs";
import * as express from "express";

//#region src/adapters/express.d.ts

type CreateExpressContextOptions = NodeHTTPCreateContextFnOptions<express.Request, express.Response>;
declare function createExpressMiddleware<TRouter extends AnyRouter>(opts: NodeHTTPHandlerOptions<TRouter, express.Request, express.Response>): express.Handler;
//# sourceMappingURL=express.d.ts.map

//#endregion
export { CreateExpressContextOptions, createExpressMiddleware };
//# sourceMappingURL=express.d.cts.map