
/**
 * 次の処理の実行を遅らせます。
 * @param ms 処理を遅らせる時間(ミリ秒)
 */
export function sleep(ms: number): Promise<void> {
    return new Promise((resolve) => {
        return setTimeout(resolve, ms)
    })
}

/**
 * URLのパラメータを取得します。
 */
export function getURLQuery(): string[][] {
    const param:string = location.search
    const usp:string[][] = [...new URLSearchParams(param).entries()]
    return usp    
}

/**
 * URLのパラメータを設定します。
 * @param param 設定するパラメータ
 */
export function setURLQuery(param:string[][]){
    const query:string = '?' + param.map((e) => `${e[0]}=${e[1]}`).join('&')
    const urlpath:string = location.pathname
    history.pushState("","",urlpath+query)

}
