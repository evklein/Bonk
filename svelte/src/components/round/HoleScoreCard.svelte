<script lang="ts">
    import type { EventHandler } from "svelte/elements";
    import type { HoleData } from "../../models/HoleData";
    import type { HoleScore } from "../../models/HoleScore";
    import * as geo from "../../services/geo";
    import * as api from "../../services/api";
    import type { CourseData } from "../../models/CourseData";
    import type { RoundData } from "../../models/RoundData";

    // Props
    export let course: CourseData;
    export let round: RoundData;
    export let hole: HoleData;
    export let holeScore: HoleScore;
    export let handleGoToNextHole: Function;
    export let handleGoToPreviousHole: Function;
    export let handleAdvance: Function;
    export let selectedPoints: [number, number][];

    let clubs: string[] = ['62°', '56°', '50°', 'P', '9', '8', '7', '6', '5', '4H', '3H', '3W', 'D'].reverse();

    function createStrokesAndPutts(event: any) {
        holeScore.strokes = [];
        holeScore.putts = [];

        if (holeScore.numberOfStrokes && holeScore.numberOfPutts) {
            for (let i = 0; i < holeScore.numberOfStrokes - holeScore.numberOfPutts; i++) {
                holeScore.strokes.push({
                    strokeNumber: i + 1,
                    penalty: false,
                });
            }
    
            for (let i = 0; i < holeScore.numberOfPutts; i++) {
                holeScore.putts.push({
                    strokeNumber: i + holeScore.numberOfStrokes + 1,
                });
            }
        }
    }

    async function saveAll() {
        console.log(holeScore);
        console.log(round);
        console.log(hole);
        // Save Hole Stats
        if (round.id && hole.id) {
            console.log('Saving stats');
            console.log(holeScore.stats);
            await api.saveHoleStats(round.id, hole.id, holeScore.stats);
        }

        let nextSelectedPointIndex = 0;
        holeScore.strokes.forEach(async stroke => {
            if (round.id && hole.id) {
                stroke.startCoordinate = selectedPoints[nextSelectedPointIndex];
                stroke.endCoordinate = selectedPoints[nextSelectedPointIndex + 1];
                stroke.distance = geo.getDistanceFromLatLonInYards(stroke.startCoordinate[0], stroke.startCoordinate[1], stroke.endCoordinate[0], stroke.endCoordinate[1]);
                await api.saveStroke(round.id, hole.id, stroke);
            }
        });

        holeScore.putts.forEach(async putt => {
            if (round.id && hole.id) {
                console.log('Saving putts');
                await api.savePutt(round.id, hole.id, putt);
            }
        });
    }

    async function saveAndGoToNext() {
        console.log('Saving!');
        await saveAll();
        handleGoToNextHole();
        console.log(hole.holeNumber);
        console.log(round.holesCompleted);
    }

    async function saveAndGoToPrevious() {
        await saveAll();
        handleGoToPreviousHole();
    }

    async function advance() {
        await saveAll();
        handleAdvance();
    }

    function clicker() {
        console.log("click");
        console.log(holeScore.stats);
    }
</script>
{#if holeScore}
<div class="card">
    <div class="card-body">
        <h5 class="card-title">
            <span class="card-title-emphasize">Hole {hole?.holeNumber}</span> // {course.name}
            <span class="par-badge badge text-bg-success">Par {hole?.par}</span>
        </h5>
        <p class="approximate-yardage">
            <i class="fas fa-arrows-alt-h"></i>
            {#if selectedPoints.length > 0 && hole.centerGreenPoint}
                {geo.getDistanceFromLatLonInYards(selectedPoints[0][0], selectedPoints[0][1], hole.centerGreenPoint[0], hole.centerGreenPoint[1]).toFixed(0)} yards
            {:else}
                -
            {/if}
        </p>
        <div class="score-entry">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th scope="col">S</th>
                        <th scope="col">P</th>
                        <th scope="col">GIR</th>
                        <th scope="col">GLD</th>
                        <th scope="col">SCR</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="td-20">
                            <input type="text"
                                class="stats-control form-control"
                                bind:value={holeScore.numberOfStrokes}
                                aria-label="strokes">
                        </td>
                        <td class="td-20">
                            <input type="text"
                                class="stats-control form-control"
                                bind:value={holeScore.numberOfPutts}
                                on:change|preventDefault={createStrokesAndPutts}
                                aria-label="putts">
                        </td>
                        <td class="td-20">
                            <input class="score-checkbox form-check-input"
                                type="checkbox"
                                on:click={clicker}
                                bind:checked={holeScore.stats.greenInRegulation}>
                        </td>
                        <td class="td-20">
                            <input class="score-checkbox form-check-input"
                                type="checkbox"
                                bind:checked={holeScore.stats.greenLightDrive}>
                        </td>
                        <td class="td-20">
                            {#if holeScore.stats && holeScore.stats.greenInRegulation}
                                <span class="disabled-checkbox-placeholder">-</span>
                            {:else}
                                <input class="score-checkbox form-check-input"
                                    type="checkbox"
                                    bind:checked={holeScore.stats.scrambling}>
                            {/if}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="shot-entry">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th style="width: 30px" scope="col">Stroke</th>
                        <th scope="col">Club</th>
                        <th scope="col">Distance (Yards)</th>
                        <th scope="col">To Center</th>
                        <th scope="col">Penalty</th>
                    </tr>
                </thead>
                <tbody>
                    {#if holeScore?.strokes && holeScore?.putts}
                        {#each {length: holeScore.strokes.length} as _, strokeNumber}
                            <tr>
                                <td>{strokeNumber + 1}</td>
                                <td>
                                    <select
                                        class="form-select"
                                        id="floatingSelect"
                                        aria-label="club-select"
                                        bind:value={holeScore.strokes[strokeNumber].club}
                                    >
                                        <option selected>Club</option>
                                        {#each clubs as club}
                                            <option value={club}>
                                                {club}
                                            </option>
                                        {/each}
                                    </select>
                                </td>
                                <td>
                                    {#if selectedPoints && selectedPoints.length >= strokeNumber + 2}
                                        {geo.getDistanceFromLatLonInYards(
                                            selectedPoints[strokeNumber][0],
                                            selectedPoints[strokeNumber][1],
                                            selectedPoints[strokeNumber + 1][0],
                                            selectedPoints[strokeNumber + 1][1]
                                        ).toFixed(1)}
                                    {/if}
                                </td>
                                <td>
                                    {#if selectedPoints && selectedPoints.length >= strokeNumber + 2 && hole && hole.centerGreenPoint}
                                        {geo.getDistanceFromLatLonInYards(
                                            hole.centerGreenPoint[0],
                                            hole.centerGreenPoint[1],
                                            selectedPoints[strokeNumber + 1][0],
                                            selectedPoints[strokeNumber + 1][1]
                                        ).toFixed(1)}
                                    {/if}
                                </td>
                                <td>
                                    <input class="penalty-checkbox form-check-input"
                                            type="checkbox" value="" id="flexCheckDefault">
                                    </td>
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
        <div class="putting-entry">
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th style="width: 30px" scope="col">Stroke</th>
                        <th scope="col">Putt</th>
                        <th scope="col">Distance (Feet)</th>
                    </tr>
                </thead>
                <tbody>
                    {#if holeScore?.strokes && holeScore?.putts}
                        {#each {length: holeScore.putts.length ?? 0} as _, i}
                        <tr>
                            <td>{holeScore.strokes.length - holeScore.putts.length + i + 1}</td>
                            <td>{i + 1}</td>
                            <td>
                                <input class="form-control" type="text" placeholder="" />
                            </td>
                        </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
        <div class="card-buttons">
            <a href="/" class="btn btn-secondary"><i class="fas fa-redo"></i> Start over</a>

        <div class="card-right">
             {#if hole?.holeNumber !== 1}
                <a href="/"
                    on:click|preventDefault={saveAndGoToPrevious}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-left"></i> Previous
                </a>
            {/if}
            {#if hole?.holeNumber < round.holesCompleted}
                <a href="/"
                    on:click|preventDefault={saveAndGoToNext}
                    class="btn btn-success">
                    <i class="fa-solid fa-arrow-right"></i> Save and go to next
                </a>
            {:else}
                <a href="/"
                    on:click|preventDefault={advance}
                    class="btn btn-success">
                    <i class="fa-solid fa-check"></i> Finish Round
                </a>
            {/if}
        </div>
        </div>
    </div>
</div>
{/if}
<style>
    .approximate-yardage {
        font-size: 12pt;
    }
    .score-checkbox {
        width: 1.75em;
        height: 1.75em;
        display: block;
        margin: auto;
        margin-top: 5px;
    }
    .penalty-checkbox {
        width: 1.75em;
        height: 1.75em;
        display: block;
        margin: auto;
        margin-top: 5px;
    }
    .penalty-checkbox:checked {
        background-color: darkred !important;
        border-color: darkred !important;
    }
    .penalty-checkbox:focus {
        border-color: rgba(139, 0, 0, .25);
        box-shadow: 0 0 0 .25rem rgba(139, 0, 0,.25)
    }
    .card-title-emphasize {
        font-size: 18pt;
        font-weight: bold;
    }
    .par-badge {
        float: right;
    }
    .card-right {
        float: right;
    }
    .stats-control {
        border: 0;
    }
    .score-entry {
        width: 300px;
    }
    .shot-entry {
        width: 400px;
    }
    .putting-entry {
        width: 250px;
    }
    td.td-20 {
        width: 20%;
    }
    .disabled-checkbox-placeholder {
        text-align: center;
        font-size: 18pt;
        color: #555;
        display: block;
        margin: auto;
    }
</style>